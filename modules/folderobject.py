from modules.enumerators import Constants,Status,FolderObjectType
from pathlib import WindowsPath
import os

class FolderObject():
    def __init__(self,path_as_windows_path: WindowsPath) -> None:
      self.path_as_string = str(path_as_windows_path)
      self.object_name = path_as_windows_path.parts[-1]
      self.type = FolderObjectType.FOLDER if path_as_windows_path.is_dir() else FolderObjectType.FILE
      self.size = os.stat(self.path_as_string).st_size
      self.folder_object_status = Constants.OK if self.type==FolderObjectType.FOLDER else self.is_file_moved(self.path_as_string)
      self.operation_status = Status.ADD_DONE if self.folder_object_status!=Constants.NOT_COMPLETE else Status.ADD_INIT

    def __eq__(self, other) -> bool:
        if not isinstance(other,FolderObject):
            return NotImplemented
        return  self.path_as_string == other.path_as_string

    def __str__(self) -> str:
        return f'{self.path_as_string} {self.type} {self.size} folder_object_status:{self.folder_object_status} {self.operation_status}'

    def set_folder_object_status(self, folder_object_status: Constants) -> None:
        self.folder_object_status = folder_object_status

    def set_operation_status(self, operation_status: Status) -> None:
        self.operation_status = operation_status

    def set_size(self, size: int) -> None:
        self.size = size
    
    def get_folder_object_status(self) -> Constants:
        return self.folder_object_status
    
    def get_operation_status(self) -> Status:
        return self.operation_status

    def get_size(self) -> int:
        return self.size
    
    def get_type(self) -> FolderObjectType:
        return self.type

    def get_path_as_string(self) -> str:
        return self.path_as_string
    
    def get_object_name(self)  -> str:
        return self.object_name

    def is_contained_in_list(self, folder_objects: list) -> bool:
        return True if len([ folder_object for folder_object in folder_objects if folder_object.__eq__(self)]) else False
    
    def get_folder_object_from_list(self, folder_objects: list) -> object:
        return [ folder_object for folder_object in folder_objects if folder_object.__eq__(self)][0]
    
    def is_file_moved(self, file_name: str) -> Constants:
        try:
            with open(file_name, 'rb') as file:
                return Constants.OK
        except PermissionError:
            return Constants.NOT_COMPLETE
        except OSError:
            return Constants.NOT_EXIST