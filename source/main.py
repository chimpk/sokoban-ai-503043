import sys
import argparse
from source.gui.game import SokobanGameApp
from source.experiment.benchmark import run_benchmark

def main():
    """
    Entry point cho Task 1:
      - Nhận đường dẫn map từ argument hoặc mặc định.
      - Chạy giải thuật tìm kiếm hoặc mở GUI Pygame.
    """
    # TODO: Member 1 & 4 integrate and run
    parser = argparse.ArgumentParser(description="Sokoban Solver App - 503043 Intro to AI")
    parser.add_argument('--map', type=str, default='source/maps/map1.txt', help='Đường dẫn tới file map')
    parser.add_argument('--mode', type=str, choices=['gui', 'benchmark'], default='gui', help='Chế độ chạy: gui hoặc benchmark')
    parser.add_argument('--maps_dir', nargs='+', default=['source/maps/map1.txt'], help='Danh sách các file map dùng cho benchmark')

    args = parser.parse_args()
    print("Sokoban Solver App - 503043 Intro to AI")

    if args.mode == 'gui':
        print(f"Đang khởi động GUI với map: {args.map}")
        app = SokobanGameApp(map_path=args.map)
        app.run()
    elif args.mode == 'benchmark':
        print("Đang chạy Benchmark...")
        run_benchmark(map_files=args.maps_dir, output_csv="results.csv")

if __name__ == "__main__":
    main()