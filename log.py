import logging
import os

class Log():

    # --- Construtor ----------------------------------------------------------
    def __init__(self):

        # --- Diretório atual ---
        diretorio = os.path.dirname(os.path.abspath(__file__))

        # ---------------------------------------------------------------------

        # --- Inicia logs DEBUG ---
        self.debug = logging.getLogger('DEBUG')
        self.debug.setLevel(logging.DEBUG)

        # --- Informa onde será guardado os logs ---
        fhd = logging.FileHandler(diretorio + '/logs/debug.log')
        fhd.setLevel(logging.DEBUG)

        # --- Formato do log ---
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        fhd.setFormatter(formatter)

        # --- Se o handler já existir apaga primeiro para depois recriar ---
        if self.debug.hasHandlers():
            self.debug.handlers.clear()

        self.debug.addHandler(fhd)

        #----------------------------------------------------------------------

        # --- Inicia log de ERROR ---
        self.error = logging.getLogger('ERROR')
        self.error.setLevel(logging.ERROR)

        # --- Informa onde será guardado os logs ---
        fhe = logging.FileHandler(diretorio + '/logs/error.log')
        fhe.setLevel(logging.ERROR)

        # --- Formato do log ---
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        fhe.setFormatter(formatter)

        # --- Se o handler já existir apaga primeiro para depois recriar ---
        if self.error.hasHandlers():
            self.error.handlers.clear()

        self.error.addHandler(fhe)

        #----------------------------------------------------------------------

        # --- Inicia log de INFO ---
        self.info = logging.getLogger('INFO')
        self.info.setLevel(logging.INFO)

        # --- Informa onde será guardado os logs ---
        fhi = logging.FileHandler(diretorio + '/logs/info.log')
        fhi.setLevel(logging.INFO)

        # --- Formato do log ---
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        fhi.setFormatter(formatter)

        # --- Se o handler já existir apaga primeiro para depois recriar ---
        if self.info.hasHandlers():
            self.info.handlers.clear()

        self.info.addHandler(fhi)