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
ImageFile.LOAD_TRUNCATED_IMAGES = True

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   
os.environ["CUDA_VISIBLE_DEVICES"] = "0" # GPU number setting

class CocoTrainer(DefaultTrainer):
  @classmethod
  def build_evaluator(cls, cfg, dataset_name, output_folder=None):

    if output_folder is None:
        os.makedirs("coco_eval", exist_ok=True)
        output_folder = "coco_eval"

    return COCOEvaluator(dataset_name, cfg, False, output_folder)

register_coco_instances("vehicle_train_PS", {}, 
                        "../../datasets/train_PS50.json", 
                        "../../datasets/train_PS")
register_coco_instances("vehicle_test_PS", {}, 
                        "../../datasets/test_PS10.json", 
                        "../../datasets/test_PS")

vehicle_train_metadata = MetadataCatalog.get("vehicle_train_PS")
dataset_dicts = DatasetCatalog.get("vehicle_train_PS")

vehicle_test_metadata = MetadataCatalog.get("vehicle_test_PS")
dataset_dicts = DatasetCatalog.get("vehicle_test_PS")


cfg = get_cfg()
cfg.merge_from_file("../configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.DATASETS.TRAIN = ("vehicle_train_PS",)
cfg.DATASETS.TEST = ("vehicle_test_PS",)

cfg.OUTPUT_DIR = "./output_PS/"
cfg.DATALOADER.NUM_WORKERS = 8
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.0003
cfg.SOLVER.WARMUP_ITERS = 130000
cfg.SOLVER.MAX_ITER =  300000
cfg.SOLVER.STEPS = []
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 32
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3
cfg.TEST.EVAL_PERIOD = 10000

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

trainer = CocoTrainer(cfg)
trainer.resume_or_load(resume=True)
trainer.train()
