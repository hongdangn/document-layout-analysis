import os
import shutil
import argparse

def copy_images_from_DocLayNet2COCO(train_path: str, 
                                    val_path: str, 
                                    PNG_path: str,
                                    train=True):
  
  COCO_path = train_path if train else val_path
  COCO_images_path = os.path.join(COCO_path, "images")

  if not os.path.exists(os.path.join(COCO_path, "images")):
    os.makedirs(os.path.join(COCO_path, "images"))

  for image_name in os.listdir(os.path.join(COCO_path, "labels")):
    # ex image_name: 01_2022_TTBTTTT_503597_page_0.txt
    image = image_name.replace(".txt", ".png")
    image_path = os.path.join(PNG_path, image)

    if not os.path.exists(os.path.join(COCO_images_path, image)):
      shutil.copy(image_path, COCO_images_path)
      
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--train_path", 
                        required=True)
    parser.add_argument("--val_path",
                        required=True)
    parser.add_argument("--PNG_path",
                        required=True)
    
    args = parser.parse_args()

    copy_images_from_DocLayNet2COCO(args.train_path,
                                    args.val_path,
                                    args.PNG_path,
                                    train=False)
    copy_images_from_DocLayNet2COCO(args.train_path,
                                    args.val_path,
                                    args.PNG_path,
                                    train=True)