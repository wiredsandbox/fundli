import os

from decouple import config
from jinja2 import Environment, FileSystemLoader


#  function to get the base path to filestorage folder
def get_file_base_path(template_folder: str):
    # get the current working directory
    cwd = os.getcwd()
    # check if the folder exists
    if not os.path.exists(os.path.join(cwd, template_folder)):
        # create the folder
        os.mkdir(os.path.join(cwd, template_folder))
    # return the path
    return os.path.join(cwd, template_folder)


PORT = config("PORT", default=7000, cast=int)
DOMAIN_NAME = str(config("DOMAIN_NAME")) + str(PORT)
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
SECRET_KEY = str(config("SECRET_KEY"))
DATABASE_URI = str(config("DATABASE_URI"))
DATABASE_NAME = str(config("DATABASE_NAME"))
STORAGE_BASE_FOLDER = get_file_base_path(str(config("STORAGE_BASE_FOLDER")))
MAIL_URL = str(config("MAIL_URL"))
MAIL_API_KEY = str(config("MAIL_API_KEY"))
TEMPLATE_FOLDER = get_file_base_path(str(config("TEMPLATE_FOLDER")))


# set the jinja2 environment
EMAIL_FILE_PATH = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER + "/email"))
