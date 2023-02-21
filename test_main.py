import main


settings = main.Settings()
game_map = main.Map()


def test_settings():
    # Window resolution
    assert settings.size == (1024, 512)
    # Pygame title
    assert settings.title == "Ray-Casting Demo"
    

def test_map():
    # Horizontal, width of the map (times block size)
    assert game_map._map_x == 8
    # Vertical, length of the map (times block size)
    assert game_map._map_y == 8
    # Size of each block
    assert game_map._block_size == 64
    # Length of the map array, map_x times map_y
    assert len(game_map._map) == 64 

    # Custom get map function, to use inside move function
    assert len(game_map.get_map()) == 64