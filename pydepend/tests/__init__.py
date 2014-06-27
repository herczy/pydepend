import os.path


def get_asset_path(name):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'assets', name)
    )
