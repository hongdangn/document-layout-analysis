import os
import shutil
import argparse
import json

def make_yolo_dataset_dir(train_path, val_path):
    if not os.path.exists(train_path):
      os.makedirs(train_path)

    if not os.path.exists(val_path):
      os.makedirs(val_path)
  
    if not os.path.exists(os.path.join(train_path, "labels")):
      os.makedirs(os.path.join(train_path, "labels"))

    if not os.path.exists(os.path.join(val_path, "labels")):
      os.makedirs(os.path.join(val_path, "labels"))

def normalize(image_size, bbox):
  """
     input box: [x_left, y_left, width, height]
     image_size: [img_width, img_height]
  """
  # return box: [x_center_norm, y_center_norm, width_norm, height_norm]

  x_center = (bbox[0] + bbox[2]/2)/image_size[0]
  y_center = (bbox[1] + bbox[3]/2)/image_size[1]
  width, height = bbox[2]/image_size[0], bbox[3]/image_size[1]

  return [x_center, y_center, width, height]


def write_info_to_file(train_path, val_path,
                       train_info, val_info,
                       train=True):
  """
     - write into labels_folder image file (type: .txt)
     - train_info, val_info: json file
     - each line in the image file is infor about a bbox in the image:
        category_id x_center y_center width height
  """

  labels_path = train_path + "/labels" if train else val_path + "/labels"
  path_info = train_info if train else val_info
  images_info = json.load(open(path_info))

  mark, num_annots = 0, len(images_info["annotations"])
  annots = images_info["annotations"]

  for image_info in images_info["images"]:
    image_name = image_info["file_name"]
    type_file = image_name[image_name.find('.') :] # type_image: .jpg, .png

    image_txt_name = image_name.replace(type_file, ".txt")

    image_txt_file = os.path.join(labels_path, image_txt_name)
    # os.makedirs(image_txt_file)
    
    image_size = [image_info["width"], image_info["height"]]

    with open(image_txt_name, "w") as file:
      for id in range(mark, num_annots):
        if annots[id]["image_id"] == image_info["id"]:
          bbox = annots[id]["bbox"]
          category_id = annots[id]["category_id"]

          norm_box = normalize(image_size, bbox)
          file.write(str(category_id)); file.write(" ")
          for i in range(len(norm_box)):
            if i < len(bbox) - 1:
              file.write(str(norm_box[i])); file.write(" ")
            else:
              file.write(str(norm_box[i])); file.write("\n")
          mark += 1
        else:
          break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--train_path", 
                        required=True)
    parser.add_argument("--val_path",
                        required=True)
    parser.add_argument("--train_json", 
                    required=True)
    parser.add_argument("--val_json", 
                        required=True)
    parser.add_argument("--folder", 
                    required=True)
    
    args = parser.parse_args()

    make_yolo_dataset_dir(args.train_path, args.val_path)

    shutil.copy(args.train_json, args.folder)
    shutil.copy(args.val_json, args.folder)

    write_info_to_file(args.train_path, args.val_path,
                       args.train_json, args.val_json,
                       train=True)
    
    write_info_to_file(args.train_path, args.val_path,
                       args.train_json, args.val_json,
                       train=False)