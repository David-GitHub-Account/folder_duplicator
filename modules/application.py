from modules.logger import Logger
from modules.enumerators import Constants,Status,FolderObjectType
from modules.monitorfolder import MonitorFolder
from modules.copyfolder import CopyFolder
from pathlib import Path
from time import sleep
import keyboard
import os

class Application():
    def __init__(self,arguments: dict) -> None:
        self.initialize_logger(arguments)
        if(self.no_input_arguments(arguments)):
            self.SOURCE_LOCATION = Path("c:/git/test/main")
            self.DESTINATION_LOCATION = Path("c:/git/test/copy")
            self.SYNCHRONIZATION_INTERVAL = 2
            choice = input("Do you want to launch the application with default setting (Y/N)?")
            if(choice == 'Y' or choice == 'y'):
                self.STATUS = Constants.DEFAULT
            else:
                self.STATUS = Constants.EROOR
        else:
            if(self.validate_arguments(arguments)):
                self.SOURCE_LOCATION = Path(arguments["source_path"])
                self.DESTINATION_LOCATION = Path(arguments["destination_path"])
                self.SYNCHRONIZATION_INTERVAL = float(arguments["synchronization_interval"])
                self.STATUS = Constants.OK
            else:
                self.STATUS = Constants.EROOR
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

    def initialize_logger(self,arguments: dict) -> None:
        log_path_key = "log_path"
        if arguments[log_path_key] is not None and os.path.exists(arguments[log_path_key]):
            self.logger = Logger.set_logger('record',Path(arguments[log_path_key]))
        else:
            self.logger = Logger.set_logger('record',Path("./"))
            if arguments[log_path_key] is None:
                self.logger.warning(f"Log file argument not provided, log'll be stored into same folder as executed python application!")
            elif not os.path.exists(arguments[log_path_key]):
                self.logger.warning(f"Provided log path doesn't exist, log'll be stored into same folder as executed python application!")
        del arguments[log_path_key]

    def validate_arguments(self,arguments: dict) -> bool:
        result = True
        for argument_key in arguments.keys():
            if "path" in argument_key:
                if arguments[argument_key] is None:
                    self.logger.error(f"Argument \"{argument_key}\" wasn't specified!")
                    result = False
                elif not os.path.exists(arguments[argument_key]):
                    self.logger.error(f"Inserted {argument_key.replace("_path","")} folder doesn't exist!")
                    result = False
            elif "interval" in argument_key:
                if arguments[argument_key] is None:
                    self.logger.error(f"Synchronization interval wasn't specified, requested value should be float number bigger than 0.1!")
                    result = False
                elif not arguments[argument_key].isdigit() or float(arguments[argument_key]) < 0.1 :
                    self.logger.error(f"Inserted value \"{arguments[argument_key]}\" must be float number bigger than 0.1!")
                    result = False
        return result
    
    def no_input_arguments(self, arguments: dict) -> bool:
        return len([argument_value for argument_value in arguments.values() if argument_value is None])==len(arguments)
    
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