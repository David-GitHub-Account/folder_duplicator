from modules.folderobject import FolderObject
from modules.enumerators import Status,Constants
from pathlib import Path
import os

class MonitorFolder():
    def __init__(self,application):
        self.SOURCE_LOCATION = application.SOURCE_LOCATION
        self.current_folder_objects=[]
        self.previous_folder_objects=[]

    def check_folder_content(self) -> list:
        self.remove_previous_folder_objects_with_status_remove()
        self.update_current_folder_objects()
        self.compare_previous_and_current_folder_objects()
        return self.current_folder_objects

    def remove_previous_folder_objects_with_status_remove(self) -> list:
        self.previous_folder_objects = [folder_object for folder_object in self.previous_folder_objects if folder_object.get_operation_status()!=Status.REMOVE]

    def update_current_folder_objects(self) -> None:
        self.current_folder_objects.clear()
        for object_windows_path in Path(self.SOURCE_LOCATION).rglob("*"):
            folder_object = FolderObject(object_windows_path)
            if(folder_object.get_folder_object_status()==Constants.NOT_EXIST):
                continue
            if(not folder_object.is_contained_in_list(self.previous_folder_objects)):
                self.current_folder_objects.append(folder_object)
            else:
                refference_folder_object = folder_object.get_folder_object_from_list(self.previous_folder_objects)
                if refference_folder_object.get_operation_status()==Status.ADD_INIT and folder_object.get_folder_object_status()==Constants.NOT_COMPLETE:
                    refference_folder_object.set_operation_status(Status.ADD_IN_PROGRESS)
                elif (refference_folder_object.get_operation_status()==Status.ADD_IN_PROGRESS or refference_folder_object.get_operation_status()==Status.ADD_INIT) and folder_object.get_folder_object_status()==Constants.OK:
                    refference_folder_object.set_operation_status(Status.ADD_DONE)
                    refference_folder_object.set_folder_object_status(Constants.OK)
                elif refference_folder_object.get_operation_status()==Status.ADD_DONE:
                    refference_folder_object.set_operation_status(Status.ACTIVE)
                self.current_folder_objects.append(refference_folder_object)
        
    def compare_previous_and_current_folder_objects(self) -> None:
        self.check_if_folder_objects_size_changed()
        self.check_missing_folder_objects()
        self.previous_folder_objects = self.current_folder_objects

    def check_if_folder_objects_size_changed(self) -> None:
        for folder_object in self.current_folder_objects:
            if(folder_object.is_contained_in_list(self.previous_folder_objects)):
                previous_folder_object = self.get_refference_on_folder_object_from_list(folder_object)
                if(os.stat(folder_object.path_as_string).st_size != previous_folder_object.get_size()):
                    folder_object.set_size(os.stat(folder_object.path_as_string).st_size)
                    folder_object.set_operation_status(Status.UPDATE)
                elif(os.stat(folder_object.path_as_string).st_size == previous_folder_object.get_size() and previous_folder_object.get_operation_status()==Status.UPDATE):
                    folder_object.set_operation_status(Status.ACTIVE)
    
    def check_missing_folder_objects(self) -> None:
        for previous_folder_object in self.previous_folder_objects:
            if(not previous_folder_object.is_contained_in_list(self.current_folder_objects)):
                previous_folder_object.set_operation_status(Status.REMOVE)
                self.current_folder_objects.append(previous_folder_object)

    def get_refference_on_folder_object_from_list(self,folder_object: FolderObject) -> list:
        return [folder_object_from_list for folder_object_from_list in self.previous_folder_objects if folder_object_from_list.__eq__(folder_object)][0]