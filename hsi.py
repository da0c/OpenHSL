import h5py
import numpy as np
from os import listdir, mkdir
from os.path import isdir
from PIL import Image
from scipy.io import loadmat, savemat
from typing import Optional, List


class HSImage:
    """
    HSImage(hsi, metadata)

        Hyperspectral Image which has a dimension X - Y - Z
        where Z is a count of channels.
        Data are captured along axis X.

        Parameters
        ----------
        hsi: np.ndarray
            3D-matrix which has a dimension X - Y - Z.
            where:
                X is along-axis of capturing data.
                Y is constant resolution.
                Z is a count of channels.

        wavelengths: list
            contains set of wavelengths for each layer HS
            len(wavelengths) == hsi.shape[2] !!!

        Attributes
        ----------
        data: np.ndarray

        wavelengths: list

        Examples
        --------
            arr = np.zeros((100, 100, 250))
            wavelengths = [400, 402, 404, ..., 980]

            hsi = HSImage(hsi=arr, wavelengths=wavelengths)

    """

    def __init__(self, hsi: Optional[np.ndarray], wavelengths: Optional[List]):
        """
            Inits HSI object.

            Raises
            ------
        """
        self.data = hsi
        self.wavelengths = wavelengths
    # ------------------------------------------------------------------------------------------------------------------

    def load_wavelengths(self, path_to_file: str):
        # TODO
        return []
    # ------------------------------------------------------------------------------------------------------------------

    def save_wavelengths(self, path_to_file: str):
        # TODO
        pass
    # ------------------------------------------------------------------------------------------------------------------

    def load_from_mat(self, path_to_file: str, mat_key: str):
        """
        load_from_mat(path_to_file, mat_key)

            Loads HSI from .mat file.

            Parameters
            ----------
            path_to_file: str
                Path to .mat file
            mat_key: str
                Key for field in .mat file as dict object
                mat_file['image']
            Raises
            ------

        """
        self.data = loadmat(path_to_file)[mat_key]

        try:
            wavelengths = loadmat(path_to_file)['wavelengths'][0]
        except:
            print('There isn\'t info about wavelengths')
            wavelengths = []

        self.wavelengths = wavelengths
    # ------------------------------------------------------------------------------------------------------------------

    def load_from_tiff(self, path_to_file: str):
        """
        load_from_tiff(path_to_file)

            Loads HSI from .tiff file.

            Parameters
            ----------
            path_to_file: str
                Path to .tiff file
            """
            # TODO GDAL or what?
        self.data = ...
        self.wavelengths = ...
        pass
    # ------------------------------------------------------------------------------------------------------------------

    def load_from_npy(self, path_to_file: str):
        """
        load_from_npy(path_to_file)

            Loads HSI from .npy file.

            Parameters
            ----------
            path_to_file: str
                Path to .npy file
        """
        self.data = np.load(path_to_file)
        self.wavelengths = self.load_wavelengths(path_to_file)
    # ------------------------------------------------------------------------------------------------------------------

    def load_from_h5(self, path_to_file: str, h5_key: str = None):
        """
        load_from_h5(path_to_file, h5_key)

            Loads HSI from .h5 file.

            Parameters
            ----------
            path_to_file: str
                Path to .h5 file
            h5_key: str
                Key for field in .h5 file as dict object
        """
        self.data = h5py.File(path_to_file, 'r')[h5_key]
        try:
            wavelengths = list(h5py.File(path_to_file, 'r')['wavelengths'])
        except:
            wavelengths = []
        self.wavelengths = wavelengths
    # ------------------------------------------------------------------------------------------------------------------

    def load_from_layer_images(self, path_to_dir: str):
        """
        load_from_images(path_to_dir)

            Loads HSI from images are placed in directory.

            Parameters
            ----------
            path_to_dir: str
                Path to directory with images
        """
        images_list = listdir(path_to_dir)
        hsi = []
        for image_name in images_list:
            img = Image.open(f'{path_to_dir}/{image_name}').convert("L")
            hsi.append(np.array(img))

        self.data = np.array(hsi).transpose((1, 2, 0))
        self.wavelengths = self.load_wavelengths('')
    # ------------------------------------------------------------------------------------------------------------------

    def save_to_mat(self, path_to_file: str, mat_key: str):
        """
        save_to_mat(path_to_file, mat_key)

            Saves HSI to .mat file as dictionary

            Parameters
            ----------
            path_to_file: str
                Path to saving file
            mat_key: str
                Key for dictionary
        """
        temp_dict = {mat_key: self.data, 'wavelengths': self.wavelengths}
        savemat(path_to_file, temp_dict)
    # ------------------------------------------------------------------------------------------------------------------

    def save_to_tiff(self, path_to_file: str):
        """
        save_to_tiff(path_to_file)

            Saves HSI to .tiff file

            Parameters
            ----------
            path_to_file: str
                Path to saving file
        """
        # TODO GDAL?
        ...
    # ------------------------------------------------------------------------------------------------------------------

    def save_to_h5(self, path_to_file: str, h5_key: str):
        """
        save_to_h5(path_to_file, h5_key)

            Saves HSI to .h5 file as dictionary.

            Parameters
            ----------
            path_to_file: str
                Path to saving file
            h5_key: str
                Key for dictionary
        """
        with h5py.File(path_to_file, 'w') as f:
            f.create_dataset(h5_key, data=self.data)
            f.create_dataset("wavelengths", data=self.wavelengths)
    # ------------------------------------------------------------------------------------------------------------------

    def save_to_npy(self, path_to_file: str):
        """
        save_to_npy(path_to_file)

            Saves HSI to .npy file.

            Parameters
            ----------
            path_to_file: str
                Path to saving file
        """
        np.save(path_to_file, self.data)
        self.save_wavelengths(path_to_file)
    # ------------------------------------------------------------------------------------------------------------------

    def save_to_images(self, path_to_dir: str, format: str = 'png'):
        """
        save_to_images(path_to_dir, format)

            Saves HSI to .npy file

            Parameters
            ----------
            path_to_dir: str
                Path to saving file
            format: str
                Format of images (png, jpg, jpeg, bmp)
        """
        if not isdir(path_to_dir):
            mkdir(path_to_dir)
        for i in range(self.data.shape[-1]):
            if format in ('png', 'jpg', 'jpeg', 'bmp'):
                Image.fromarray(self.data[:, :, i]).convert("L").save(f'{path_to_dir}/{i}.{format}')
            else:
                raise Exception('Unexpected format')
    # ------------------------------------------------------------------------------------------------------------------
