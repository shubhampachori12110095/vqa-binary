import json
import os
import argparse
import progressbar as pb

parser = argparse.ArgumentParser()
parser.add_argument('question_json_path')
parser.add_argument('annotation_json_path')
parser.add_argument('image_folder_path')
parser.add_argument('target_path')
parser.add_argument('--prefix', default="COCO_train2014_")
parser.add_argument('--id_len', default=12, type=int)
parser.add_argument('--ext', default='.jpg')

ARGS = parser.parse_args()


def prepro_common(args):
    question_json_path = args.question_json_path
    annotation_json_path = args.annotation_json_path
    image_folder_path = args.image_folder_path
    id_len = args.id_len
    prefix = args.prefix
    ext = args.ext
    target_path = args.target_path

    print "Loading %s ..." % question_json_path
    question_json = json.load(open(question_json_path, 'rb'))
    print "Loading %s ..." % annotation_json_path
    annotation_json = json.load(open(annotation_json_path, 'rb'))
    question_list = []
    multiple_choices_list = []
    answer_list = []
    image_index_list = []
    image_path_list = []
    image_path_dict = {}

    num_questions = len(question_json['questions'])

    pbar = pb.ProgressBar(widgets=[pb.Percentage(), pb.Bar(), pb.Timer()], maxval=num_questions).start()

    for idx, (question_dict, annotation_dict) in enumerate(zip(question_json['questions'], annotation_json['annotations'])):
        question_id = question_dict['question_id']
        assert question_id == annotation_dict['question_id']
        image_id = question_dict['image_id']
        assert image_id == annotation_dict['image_id']
        question = question_dict['question']
        multiple_choices = question_dict['multiple_choices']
        answer = annotation_dict['multiple_choice_answer']
        image_id_str = str(image_id).zfill(id_len)
        image_path = os.path.join(image_folder_path, "%s%s%s" % (prefix, image_id_str, ext))

        question_list.append(question)
        multiple_choices_list.append(multiple_choices)
        answer_list.append(answer)
        if image_path in image_path_dict:
            image_index_list.append(image_path_dict[image_path])
        else:
            image_index_list.append(len(image_path_list))
            image_path_dict[image_path] = len(image_path_list)
            image_path_list.append(image_path)

        pbar.update(idx + 1)

    pbar.finish()

    if not os.path.exists(target_path):
        os.mkdir(target_path)

    print "Dumping json files ..."
    json.dump(question_list, open(os.path.join(target_path, "question_list.json"), 'w'))
    json.dump(multiple_choices_list, open(os.path.join(target_path, "multiple_choices_list.json"), 'w'))
    json.dump(answer_list, open(os.path.join(target_path, "answer_list.json"), 'w'))
    json.dump(image_path_list, open(os.path.join(target_path, "image_path_list.json"), 'w'))
    json.dump(image_index_list, open(os.path.join(target_path, "image_index_list.json"), 'w'))

if __name__ == "__main__":
    prepro_common(ARGS)