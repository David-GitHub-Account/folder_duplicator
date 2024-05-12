from modules.enumerators import Status,FolderObjectType
import os
import shutil
from pathlib import Path

class CopyFolder():
    def __init__(self,application) -> None:
        self.SOURCE_LOCATION = application.SOURCE_LOCATION
        self.DESTINATION_LOCATION = application.DESTINATION_LOCATION
        self.folder_object = None
        self.create_destination_location()
    
    def create_destination_location(self):
        if not os.path.exists(self.DESTINATION_LOCATION):
            os.makedirs(self.DESTINATION_LOCATION)

    def process_folder_objects(self,folder_objects: list) -> None:
        self.process_folders(folder_objects)
        self.process_files(folder_objects)

    def provide_folder_objects_list_by_type(self, folder_objects: list, type: FolderObjectType) -> list:
        return [folder_object for folder_object in folder_objects if folder_object.get_type()==type] 

    def get_source_location_from_folder_object(self) -> Path:
        return Path(self.folder_object.get_path_as_string())
    
    def get_destination_location_from_folder_object(self) -> Path:
        return Path(str(self.get_source_location_from_folder_object()).replace(str(self.SOURCE_LOCATION),str(self.DESTINATION_LOCATION)))
    
    def process_folders(self,folder_objects: list) -> None:
        folder_objects = self.provide_folder_objects_list_by_type(folder_objects, FolderObjectType.FOLDER)
        for self.folder_object in folder_objects:
            destination_location = self.get_destination_location_from_folder_object()
            if os.path.exists(destination_location) and self.folder_object.get_operation_status()==Status.REMOVE:
                shutil.rmtree(destination_location, ignore_errors=True)
            elif not os.path.exists(destination_location) and (self.folder_object.get_operation_status()==Status.ADD_DONE or self.folder_object.get_operation_status()==Status.ACTIVE):
                os.makedirs(destination_location)
    
    def process_files(self,folder_objects: list) -> None:
        folder_objects = self.provide_folder_objects_list_by_type(folder_objects, FolderObjectType.FILE)
        for self.folder_object in folder_objects:
            source_location = self.get_source_location_from_folder_object()
            destination_location = self.get_destination_location_from_folder_object()
            if not os.path.exists(destination_location) and self.folder_object.get_operation_status()==Status.ACTIVE:
                shutil.copyfile(source_location, destination_location)
            elif os.path.exists(destination_location) and self.folder_object.get_operation_status()==Status.UPDATE:
                os.remove(destination_location)
                shutil.copyfile(source_location, destination_location)
            elif os.path.exists(destination_location) and self.folder_object.get_operation_status()==Status.REMOVE:
                os.remove(destination_location)