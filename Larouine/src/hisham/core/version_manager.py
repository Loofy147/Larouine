import semver

class VersionManager:
    def __init__(self):
        self.current_version = semver.VersionInfo.parse("1.0.0")
    
    def bump_version(self, change_type: str):
        """
        change_type: major/minor/patch
        """
        if change_type == 'major':
            self.current_version = self.current_version.bump_major()
        elif change_type == 'minor':
            self.current_version = self.current_version.bump_minor()
        else:
            self.current_version = self.current_version.bump_patch()
    
    def get_version(self):
        return str(self.current_version)