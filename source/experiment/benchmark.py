import csv
import time
import matplotlib.pyplot as plt

def run_benchmark(map_files: list[str], output_csv: str = "results.csv"):
    """
    Thực hiện so sánh thực nghiệm giữa UCS và A* (R3):
      - Thời gian thực thi (Execution Time).
      - Không gian bộ nhớ / Số node mở rộng (Expanded Nodes).
      - Số node sinh ra (Generated Nodes).
      - Độ lớn tối đa frontier (Max Frontier Size).
      - Chi phí lời giải (Solution Cost).

    Xuất kết quả ra file CSV và vẽ biểu đồ.
    """
    # TODO: Member 4 implement benchmark & chart plotting
    results = []
    algorithms = ["UCS", "A*"]

    for map_file in map_files:
        for algo in algorithms:
            # TODO: Import và gọi hàm giải thuật toán thật ở đây
            # Giả lập tracking dữ liệu để kiểm tra xuất CSV và Chart
            start_time = time.perf_counter()
            time.sleep(0.01) # Mô phỏng thời gian chạy
            exec_time = time.perf_counter() - start_time
            
            # Thông số ảo demo (Hãy thay bằng kết quả trả về từ file core của nhóm)
            expanded = 1200 if algo == "UCS" else 600
            generated = 3000 if algo == "UCS" else 1500
            max_frontier = 500 if algo == "UCS" else 200
            cost = 35 

            results.append({
                "Map": map_file,
                "Algorithm": algo,
                "Execution Time (s)": round(exec_time, 4),
                "Expanded Nodes": expanded,
                "Generated Nodes": generated,
                "Max Frontier Size": max_frontier,
                "Solution Cost": cost
            })

    # Xuất kết quả ra file CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Đã lưu kết quả thực nghiệm tại: {output_csv}")

    # Vẽ biểu đồ so sánh Execution Time
    plot_benchmark_charts(results)

def plot_benchmark_charts(results: list[dict]):
    """Vẽ biểu đồ so sánh hiệu năng giữa các thuật toán."""
    maps = list(set([r["Map"] for r in results]))
    ucs_times = [r["Execution Time (s)"] for r in results if r["Algorithm"] == "UCS"]
    astar_times = [r["Execution Time (s)"] for r in results if r["Algorithm"] == "A*"]

    x = range(len(maps))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar([i - width/2 for i in x], ucs_times, width=width, label='UCS', color='#ff9999')
    plt.bar([i + width/2 for i in x], astar_times, width=width, label='A*', color='#66b3ff')

    plt.title('So sánh Thời gian thực thi (Execution Time): UCS vs A*')
    plt.xlabel('Maps')
    plt.ylabel('Thời gian (s)')
    plt.xticks(x, maps, rotation=15)
    plt.legend()
    plt.tight_layout()

    # Lưu biểu đồ
    plt.savefig('benchmark_chart.png')
    print("Đã lưu biểu đồ tại: benchmark_chart.png")