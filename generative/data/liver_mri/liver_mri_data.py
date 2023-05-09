# this is a pytorch dataset class for liver mri data
# will load data from a spreadsheet and return an image
# the spreadsheet will have a column for the image path and a column for the label
# the images are .nii or .nii.gz files
# we will use torchio to load the images

from torch.utils.data import Dataset
import torchio as tio
import pandas as pd
import torch

class RandomLiverCropMRIDataset(Dataset):
    
    """
    Returns a random crop of a liver MRI image
    params:
        csv_path: path to a csv (or xlsx) file with the image paths and labels
        transform: a transform to apply to the image
        sequences: a list of sequences to load from the image. these must be columns in the csv file
        label_column: the name of the column in the csv file that contains the labels
        patch_size: the size of the patch to crop from the image (tuple)
    """
    
    def __init__(self, csv_path, sequences, label_column, patch_size, transform=None):
        self.csv_path = csv_path
        if '.csv' in csv_path:
            self.df = pd.read_csv(csv_path, index_col=0)
        elif '.xlsx' in csv_path:
            self.df = pd.read_excel(csv_path, index_col=0)
        
        assert label_column in self.df.columns, f'Label column {label_column} not in csv file'
        assert all([seq in self.df.columns for seq in sequences]), f'One or more sequences not in csv file'
        
        self.transform = transform
        self.sequences = sequences
        self.label_column = label_column
        self.patch_size = patch_size
        self.crop = tio.transforms.CropOrPad(
            patch_size,
            labels=[self.label_column]
        )
        
    def __len__(self):
        return len(self.df)
    
    def _load_subject(self, df_index):
        sequence_dict = {}
        for s in self.sequences:
            sequence_dict[s] = tio.ScalarImage(self.df.at[df_index, s])
        
        sequence_dict[self.label_column] = tio.LabelMap(self.df.at[df_index, self.label_column])
        subject = tio.Subject(sequence_dict)
        return subject
    
    def __getitem__(self, idx):
        df_idx = self.df.index[idx]
        subject = self._load_subject(df_idx)
        patch = self.crop(subject)
        
        if self.transform:
            patch = self.transform(patch)
        
        x = torch.vstack([patch[s].data for s in self.sequences])
        y = patch[self.label_column].data
        return x, y