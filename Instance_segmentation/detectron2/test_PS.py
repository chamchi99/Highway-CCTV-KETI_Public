import torch, torchvision
import numpy as np
import os, json, cv2, random
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import build_detection_test_loader
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.datasets import register_coco_instances
import detectron2
from detectron2.utils.logger import setup_logger
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from PIL import ImageFile 
from detectron2.utils.visualizer import ColorMode
import datetime
ImageFile.LOAD_TRUNCATED_IMAGES = True

now = datetime.datetime.now()
print(now)

class CocoPredictor(DefaultPredictor):
  @classmethod
  def build_evaluator(cls, cfg, dataset_name, output_folder=None):

    if output_folder is None:
        os.makedirs("coco_eval", exist_ok=True)
        output_folder = "coco_eval"

    return COCOEvaluator(dataset_name, cfg, False, output_folder)

register_coco_instances("vehicle_test_PS", {}, 
                        "../../datasets/test_PS10.json", 
                        "../../datasets/test_PS")

vehicle_test_metadata = MetadataCatalog.get("vehicle_test_PS")
dataset_dicts = DatasetCatalog.get("vehicle_test_PS")

cfg = get_cfg()
cfg.merge_from_file("../configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3
cfg.OUTPUT_DIR = "./output_PS"
cfg.MODEL.BACKBONE.FREEZE_AT = 0
cfg.MODEL.WEIGHTS = "../../weights/model_final_PS.pth"
cfg.DATASETS.TEST = ("vehicle_test_PS",)

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
os.makedirs("./output_PS", exist_ok=True)

predictor = CocoPredictor(cfg)

i=0
for d in random.sample(dataset_dicts, 5):    
    im = cv2.imread(d["file_name"])
    file_name = d["file_name"][:-4]
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                   metadata=vehicle_test_metadata, 
                   scale=0.5, 
                   instance_mode=ColorMode.IMAGE_BW
    )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imwrite(cfg.OUTPUT_DIR +"/"+str(i)+"_result.png",out.get_image()[:, :, ::-1])
    i+=1

evaluator = COCOEvaluator("vehicle_test_PS", ("bbox", "segm"), False, output_dir="./output_PS/")
test_loader = build_detection_test_loader(cfg, "vehicle_test_PS")
print(inference_on_dataset(predictor.model, test_loader, evaluator))
now = datetime.datetime.now()
print(now)
