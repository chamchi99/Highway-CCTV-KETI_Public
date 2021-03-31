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

ImageFile.LOAD_TRUNCATED_IMAGES = True

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

class CocoPredictor(DefaultPredictor):
  @classmethod
  def build_evaluator(cls, cfg, dataset_name, output_folder=None):

    if output_folder is None:
        os.makedirs("coco_eval", exist_ok=True)
        output_folder = "coco_eval"

    return COCOEvaluator(dataset_name, cfg, False, output_folder)

class CocoTrainer(DefaultTrainer):
    
  @classmethod
  def build_evaluator(cls, cfg, dataset_name, output_folder=None):

    if output_folder is None:
        os.makedirs("coco_eval", exist_ok=True)
        output_folder = "coco_eval"

    return COCOEvaluator(dataset_name, cfg, False, output_folder)

register_coco_instances("vehicle_test_BB", {}, 
                        "../../datasets/test_BB10.json", 
                        "../../datasets/test_BB")

vehicle_test_metadata = MetadataCatalog.get("vehicle_test_BB")
dataset_dicts = DatasetCatalog.get("vehicle_test_BB")

cfg = get_cfg()
cfg.merge_from_file("../configs/COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3
cfg.OUTPUT_DIR = "./output_BB"
cfg.MODEL.BACKBONE.FREEZE_AT = 0
cfg.MODEL.WEIGHTS = "../../weights/model_final_BB.pth"
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.DATASETS.TEST = ("vehicle_test_BB",)

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
os.makedirs("./output_BB", exist_ok=True)

trainer = CocoTrainer(cfg)
trainer.resume_or_load(resume=True)

##### prdiction model load #####
predictor = CocoPredictor(cfg)

i=0
for d in random.sample(dataset_dicts, 1):    
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
####################################

evaluator = COCOEvaluator("vehicle_test_BB", {"bbox"}, False, output_dir="./output_BB/")
test_loader = build_detection_test_loader(cfg, "vehicle_test_BB")
print(inference_on_dataset(trainer.model, test_loader, evaluator))