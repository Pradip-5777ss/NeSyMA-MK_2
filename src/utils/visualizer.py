import os
import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent GUI issues
import matplotlib.pyplot as plt

class MetricsVisualizer:
    def __init__(self, metrics_path: str = "data/evaluation_metrics.json", output_dir: str = "data"):
        self.metrics_path = metrics_path
        self.output_dir = output_dir

    def generate_plots(self):
        """Generates success rate and time analysis plots."""
        print(f"[INFO] Generating graphs using {self.metrics_path}...")
        
        if not os.path.exists(self.metrics_path):
            print(f"[WARN] Metrics file {self.metrics_path} not found. Skipping visualization.")
            return

        try:
            with open(self.metrics_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load metrics for visualization: {e}")
            return

        if not data:
            print("[WARN] Metrics data is empty. Skipping visualization.")
            return

        self._plot_success_pie(data)
        self._plot_time_analysis(data)

    def _plot_success_pie(self, data):
        success_count = sum(1 for item in data if item.get("final_status") == "Success")
        failed_count = sum(1 for item in data if item.get("final_status") == "Failed")
        total = len(data)

        if total == 0:
            return

        labels = ['Success', 'Failed']
        sizes = [success_count, failed_count]
        colors = ['#2ecc71', '#e74c3c']
        explode = (0.05, 0) if failed_count > 0 else (0, 0)

        plt.figure(figsize=(6, 5))
        plt.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct=lambda p: '{:.1f}%\n({:d})'.format(p, int(p*total/100)) if p > 0 else '',
            shadow=False,
            startangle=140,
            textprops={'fontsize': 12, 'weight': 'bold'}
        )
        plt.title('Refactoring Execution Success vs. Failure Rate', fontsize=14, weight='bold', pad=20)
        plt.tight_layout()
        
        plot_path = os.path.join(self.output_dir, 'success_vs_failure.png')
        plt.savefig(plot_path, dpi=150)
        plt.close()
        print(f"[INFO] Success rate pie chart saved to {plot_path}")

    def _plot_time_analysis(self, data):
        files = [os.path.basename(item.get("file", "unknown")) for item in data]
        llm_times = [item.get("llm_generation_time_ms", 0) / 1000.0 for item in data]  # convert to seconds
        z3_times = [item.get("z3_verification_time_ms", 0) / 1000.0 for item in data]  # convert to seconds

        # Limit to first 15 files if there are too many to keep the chart clean
        if len(data) > 15:
            files = files[:15]
            llm_times = llm_times[:15]
            z3_times = z3_times[:15]
            title_suffix = " (Top 15 Files)"
        else:
            title_suffix = ""

        plt.figure(figsize=(10, 6))
        
        # Stacked bar plot
        bars1 = plt.bar(files, llm_times, label='LLM Generation', color='#3498db')
        bars2 = plt.bar(files, z3_times, bottom=llm_times, label='Z3 Verification', color='#9b59b6')

        plt.ylabel('Execution Time (seconds)', fontsize=12, weight='bold')
        plt.xlabel('Files', fontsize=12, weight='bold')
        plt.title(f'Time Analysis per File{title_suffix}', fontsize=14, weight='bold', pad=15)
        plt.xticks(rotation=45, ha='right')
        plt.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        plt.tight_layout()
        plot_path = os.path.join(self.output_dir, 'time_analysis.png')
        plt.savefig(plot_path, dpi=150)
        plt.close()
        print(f"[INFO] Time analysis bar chart saved to {plot_path}")
