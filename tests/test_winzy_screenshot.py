import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch
from PIL import Image

import winzy_screenshot as w
from winzy_screenshot import ScreenshotManager
from argparse import ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args([])
    assert result.bbox is None

    result = parser.parse_args(["-b", "0", "10", "20", "50"])
    assert result.bbox == [[0, 10, 20, 50]]
    assert result.title is None
    assert result.use_tempdir == False


def test_plugin(capsys):
    w.screenshot_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out


def test_parser_with_tempdir():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)
    result = parser.parse_args(["--use-tempdir"])
    assert result.use_tempdir == True


def test_parser_with_title():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)
    result = parser.parse_args(["-t", "MyWindow"])
    assert result.title == "MyWindow"


def test_parser_with_activewindow():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)
    result = parser.parse_args(["--activewindow"])
    assert result.activewindow == True


def test_parser_multiple_bboxes():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)
    result = parser.parse_args([
        "-b", "0", "0", "50", "50",
        "-b", "50", "50", "50", "50"
    ])
    assert len(result.bbox) == 2
    assert result.bbox[0] == [0, 0, 50, 50]
    assert result.bbox[1] == [50, 50, 50, 50]


class TestScreenshotManager:
    @pytest.fixture
    def sample_image(self):
        """Create a sample 1000x1000 image for testing"""
        return Image.new('RGB', (1000, 1000), color='red')

    def test_crop_image_basic(self, sample_image):
        """Test basic image cropping with percentages"""
        manager = ScreenshotManager([])
        # Crop 50% from center (25%, 25%, 50%, 50%)
        cropped = manager.crop_image(sample_image, (25, 25, 50, 50))
        assert cropped.size == (500, 500)

    def test_crop_image_full(self, sample_image):
        """Test cropping entire image (0%, 0%, 100%, 100%)"""
        manager = ScreenshotManager([])
        cropped = manager.crop_image(sample_image, (0, 0, 100, 100))
        assert cropped.size == (1000, 1000)

    def test_crop_image_quarter(self, sample_image):
        """Test cropping quarter of image"""
        manager = ScreenshotManager([])
        # Top-left quarter
        cropped = manager.crop_image(sample_image, (0, 0, 50, 50))
        assert cropped.size == (500, 500)

    def test_crop_image_preserves_mode(self, sample_image):
        """Test that cropped image preserves original mode"""
        manager = ScreenshotManager([])
        cropped = manager.crop_image(sample_image, (0, 0, 50, 50))
        assert cropped.mode == sample_image.mode

    def test_save_image_to_tempdir(self, sample_image):
        """Test saving image to a temporary directory"""
        manager = ScreenshotManager([])
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.png")
            manager.save_image(sample_image, filename)
            assert os.path.exists(filename)
            # Verify it's a valid image
            with Image.open(filename) as img:
                assert img.size == (1000, 1000)

    def test_save_image_invalid_path(self, sample_image, caplog):
        """Test saving image to invalid path logs error"""
        manager = ScreenshotManager([])
        manager.save_image(sample_image, "/nonexistent/path/image.png")
        assert "Failed to save image" in caplog.text

    @patch('winzy_screenshot.ImageGrab.grab')
    def test_take_screenshot(self, mock_grab):
        """Test taking a screenshot"""
        mock_image = Image.new('RGB', (800, 600), color='blue')
        mock_grab.return_value = mock_image

        manager = ScreenshotManager([])
        result = manager.take_screenshot()

        assert result == mock_image
        mock_grab.assert_called_once()

    def test_screenshot_manager_initialization(self):
        """Test ScreenshotManager initialization with bboxes"""
        bboxes = [(0, 0, 50, 50), (50, 50, 50, 50)]
        manager = ScreenshotManager(bboxes)
        assert manager.bboxes == bboxes
        assert manager.esc_pressed_count == 0

    def test_crop_image_different_sizes(self):
        """Test cropping images of different sizes"""
        manager = ScreenshotManager([])

        # Test with 1920x1080 image
        img_wide = Image.new('RGB', (1920, 1080), color='green')
        cropped_wide = manager.crop_image(img_wide, (0, 0, 50, 50))
        assert cropped_wide.size == (960, 540)

        # Test with 500x500 image
        img_square = Image.new('RGB', (500, 500), color='blue')
        cropped_square = manager.crop_image(img_square, (0, 0, 50, 50))
        assert cropped_square.size == (250, 250)

    def test_crop_image_edge_cases(self, sample_image):
        """Test cropping with edge case values"""
        manager = ScreenshotManager([])

        # Test with very small percentage
        cropped = manager.crop_image(sample_image, (0, 0, 1, 1))
        assert cropped.size == (10, 10)

        # Test with offset crop
        cropped = manager.crop_image(sample_image, (10, 10, 80, 80))
        assert cropped.size == (800, 800)


class TestHelloWorld:
    def test_hello_world_name(self):
        """Test HelloWorld class name"""
        assert w.HelloWorld.__name__ == "HelloWorld"

    def test_hello_world_docstring(self):
        """Test HelloWorld class docstring"""
        assert w.HelloWorld.__doc__ == "Screenshot using python"

    def test_hello_method(self, capsys):
        """Test hello method output"""
        plugin = w.HelloWorld()
        plugin.hello(None)
        captured = capsys.readouterr()
        assert "Hello! This is an example ``winzy`` plugin." in captured.out


class TestParserComprehensive:
    def test_parser_all_arguments(self):
        """Test parser with all arguments combined"""
        subparser = ArgumentParser().add_subparsers()
        parser = w.create_parser(subparser)
        result = parser.parse_args([
            "-b", "10", "20", "30", "40",
            "--use-tempdir",
            "-t", "TestWindow",
            "--activewindow"
        ])
        assert result.bbox == [[10, 20, 30, 40]]
        assert result.use_tempdir == True
        assert result.title == "TestWindow"
        assert result.activewindow == True

    def test_parser_bbox_float_values(self):
        """Test parser with float bbox values"""
        subparser = ArgumentParser().add_subparsers()
        parser = w.create_parser(subparser)
        result = parser.parse_args(["-b", "10.5", "20.5", "30.5", "40.5"])
        assert result.bbox == [[10.5, 20.5, 30.5, 40.5]]
