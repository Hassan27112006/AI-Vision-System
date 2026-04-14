import os
import pandas as pd
import glob
import xml.etree.ElementTree as ET

def preprocess_human_faces(base_dir, output_file):
    print("Preprocessing Human Faces detection dataset...")
    df = pd.read_csv(os.path.join(base_dir, 'human-faces-object-detection', 'faces.csv'))
    # Correct columns: image_name,width,height,x0,y0,x1,y1
    df_clean = df[['image_name', 'x0', 'y0', 'x1', 'y1']].copy()
    df_clean.columns = ['filename', 'xmin', 'ymin', 'xmax', 'ymax']
    df_clean['class'] = 'face'
    df_clean.to_csv(output_file, index=False)
    print(f"Saved preprocessed human faces to {output_file}")

def preprocess_animals(base_dir, output_file):
    print("Preprocessing Animals (Cats, Dogs, Foxes) dataset...")
    animal_data = []
    # Dataset name has commas and spaces, use exact match
    animal_dir = os.path.join(base_dir, 'Animal Image Dataset-Cats, Dogs, and Foxes')
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    for animal_type in ['cat', 'dog', 'fox']:
        curr_dir = os.path.join(animal_dir, animal_type)
        if os.path.exists(curr_dir):
            for ext in extensions:
                # also check if files are directly in animal_type folder
                for img_path in glob.glob(os.path.join(curr_dir, ext)):
                    filename = os.path.basename(img_path)
                    animal_data.append([filename, animal_type, 0, 0, 0, 0])
                # check nested folders if any
                for img_path in glob.glob(os.path.join(curr_dir, '*', ext)):
                    filename = os.path.basename(img_path)
                    animal_data.append([filename, animal_type, 0, 0, 0, 0])
    
    df = pd.DataFrame(animal_data, columns=['filename', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
    df.to_csv(output_file, index=False)
    print(f"Saved preprocessed animals metadata to {output_file}")

def preprocess_generic_objects(base_dir, output_file):
    print("Preprocessing Generic Object Detection dataset...")
    obj_csv = os.path.join(base_dir, 'object-detection-dataset', 'Images Data')
    if os.path.exists(obj_csv):
        df = pd.read_csv(obj_csv)
        # Correct columns: Filename,Width,Height,Name,xmin,xmax,ymin,ymax
        df_clean = df[['Filename', 'xmin', 'ymin', 'xmax', 'ymax', 'Name']].copy()
        df_clean.columns = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class']
        df_clean.to_csv(output_file, index=False)
        print(f"Saved preprocessed generic objects to {output_file}")
    else:
        print("Warning: Object detection CSV 'Images Data' not found.")

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    preprocess_human_faces(base_dir, os.path.join(data_dir, 'human_faces_annotations.csv'))
    preprocess_animals(base_dir, os.path.join(data_dir, 'animal_annotations.csv'))
    preprocess_generic_objects(base_dir, os.path.join(data_dir, 'object_detection_annotations.csv'))

if __name__ == "__main__":
    main()
