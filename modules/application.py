from modules.logger import Logger
from modules.enumerators import Constants,Status,FolderObjectType
from modules.monitorfolder import MonitorFolder
from modules.copyfolder import CopyFolder
from pathlib import Path
from time import sleep
import keyboard

class Application():
    def __init__(self,arguments: dict) -> None:
        if(self.arguments_correct(arguments)):
            self.SOURCE_LOCATION = Path(arguments["source_path"])
            self.DESTINATION_LOCATION = Path(arguments["destination_path"])
            self.SYNCHRONIZATION_INTERVAL = int(arguments["synchronization_interval"])
            self.LOG_PATH = Path(arguments["log_path"])
            self.STATUS = Constants.OK
        else:
            self.SOURCE_LOCATION = Path("c:/git/test/main")
            self.DESTINATION_LOCATION = Path("c:/git/test/copy")
            self.SYNCHRONIZATION_INTERVAL = 2
            self.LOG_PATH = Path("c:/giti/test/logs")
            choice = input("Do you want to launch the application with default setting (Y/N)?")
            if(choice == 'Y' or choice == 'y'):
                self.STATUS = Constants.DEFAULT
            else:
                self.STATUS = Constants.EROOR
        self.logger = Logger.set_logger('record',self.LOG_PATH)
        if(self.STATUS != Constants.EROOR):
            self.monitor_folder = MonitorFolder(self)
            self.copy_folder = CopyFolder(self)

    def run(self) -> None:
        sleep_time = self.SYNCHRONIZATION_INTERVAL
        pause = 0.1
        while(not self.key_q_pressed()):
            if(sleep_time <= 0):
                folder_objects = self.monitor_folder.check_folder_content()
                self.log_all_operations(folder_objects)
                self.copy_folder.process_folder_objects(folder_objects)
                sleep_time = self.SYNCHRONIZATION_INTERVAL
            sleep_time -= pause
            sleep(pause)
        self.logger.info("The application was terminated!!")

    def arguments_correct(self,arguments: dict) -> bool:
        return len([argument_value for argument_value in arguments.values() if argument_value is None])==0
    
    def key_q_pressed(self):
        return keyboard.is_pressed('Q') or keyboard.is_pressed('q')
    
    def log_all_operations(self, folder_objects: list) -> None:
        for folder_object in folder_objects:
            type = "folder" if folder_object.get_type()==FolderObjectType.FOLDER else "file"
            if(folder_object.get_operation_status()==Status.ADD_INIT):
                self.logger.info(f"object: {folder_object.get_object_name()} type: {type} location: {folder_object.get_path_as_string()} => copying was initialized.")
            elif(folder_object.get_operation_status()==Status.ADD_DONE):
                self.logger.info(f"object: {folder_object.get_object_name()} type: {type} location: {folder_object.get_path_as_string()} => was copied")
            elif(folder_object.get_operation_status()==Status.UPDATE):
                self.logger.info(f"object: {folder_object.get_object_name()} type: {type} location: {folder_object.get_path_as_string()} => was updated.")
            elif(folder_object.get_operation_status()==Status.REMOVE):
                self.logger.info(f"object: {folder_object.get_object_name()} type: {type} location: {folder_object.get_path_as_string()} => was removed.")