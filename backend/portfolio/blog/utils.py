import math
import re


def calculate_read_time(content):
    total_read_time = 0
    for block in content:
        if block.block_type == "rich_text_block":
            total_read_time += calculate_rich_text_block_read_time(block)
        if block.block_type == "code_block":
            total_read_time += calculate_code_block_read_time(block)
        if block.block_type == "carousel_block":
            total_read_time += calculate_carousel_block_read_time(block)
    return total_read_time


def calculate_rich_text_block_read_time(block):
    words_per_minute = 265
    words = len(re.findall(r"\w+", block.value.source))
    return math.ceil(words / words_per_minute)


def calculate_code_block_read_time(block):
    words_per_minute = 100
    words = len(re.findall(r"\w+", block.value.get("code", "")))
    return math.ceil(words / words_per_minute)


def calculate_carousel_block_read_time(block):
    images_per_minute = 3
    images = len(block.value.get("images", ""))
    return math.ceil(images / images_per_minute)
