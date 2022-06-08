import os

import cv2
import numpy as np
from torch.utils.data import Dataset

from utils.io import ls


class TLessDataset(Dataset):
    """Dataset class for loading data from memory."""

    def __init__(self, path, transform=None):
        """
        Args:
            path (string): Path to the dataset.
        """
        self.transform = transform
        self.images = []
        self.labels = []

        objects = sorted(os.listdir(path))
        for o in objects:
            obj_dir = os.path.join(path, o)
            if os.path.isdir(obj_dir):
                sequences = os.listdir(obj_dir)
                for s in sequences:
                    seq_dir = os.path.join(obj_dir, s)
                    if os.path.isdir(seq_dir):
                        self.images += [os.path.join(seq_dir, p) for p in ls(seq_dir, '.png')]
                        self.labels += [os.path.join(seq_dir, p) for p in ls(seq_dir, '.npz')]

    def __len__(self):
        """Return the size of dataset."""
        return len(self.images)

    def __getitem__(self, idx):
        """Get the item at index idx."""

        # Get the data and label
        data = cv2.imread(self.images[idx])
        dmap = np.load(self.labels[idx])['dmap'].astype(np.float32)
        nmap = np.load(self.labels[idx])['nmap'].astype(np.float32)
        mask = dmap >= 1

        # Apply transformation if any
        if self.transform:
            data = self.transform(data)

        # Return the data and label
        return data, (dmap, nmap, mask)
