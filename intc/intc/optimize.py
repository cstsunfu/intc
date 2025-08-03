import random
import time

import ray
from ray import tune
from ray.tune.schedulers import ASHAScheduler

# 1. 基础配置文件 (dict)
BASE_CONFIG = {
    "model_name": "ResNet18",
    "dataset": "CIFAR-10",
    "optimizer": "Adam",
    "num_epochs": 15,
    "lr": 0.01,
    "batch_size": 64,
    "activation": "relu",
}


# 2. 可训练函数
def trainable_function(config):
    lr = config["lr"]
    batch_size = config["batch_size"]
    activation = config["activation"]
    num_epochs = config["num_epochs"]

    if activation == "relu":
        activation_factor = 0.95
    elif activation == "tanh":
        activation_factor = 0.85
    else:
        activation_factor = 0.7

    for epoch in range(num_epochs):
        score = (
            (1 / (lr * 100)) * activation_factor
            + random.uniform(-0.1, 0.1)
            - (batch_size / 512)
        )
        time.sleep(0.1)
        tune.report({"mean_accuracy": score, "epoch": epoch})


# 3. 超参数搜索空间
search_space = {
    "lr": tune.loguniform(1e-4, 1e-1),
    "batch_size": tune.choice([16, 32, 64, 128]),
    "activation": tune.choice(["relu", "tanh", "sigmoid"]),
}


# 4. 运行Tuning
def main():
    # 初始化 Ray
    ray.init(ignore_reinit_error=True)

    # 合并配置
    final_config = BASE_CONFIG.copy()
    final_config.update(search_space)

    # 配置调度器
    asha_scheduler = ASHAScheduler(
        metric="mean_accuracy",
        mode="max",
        max_t=BASE_CONFIG["num_epochs"],
        grace_period=3,
        reduction_factor=2,
    )

    # 运行
    analysis = tune.run(
        trainable_function,
        config=final_config,
        num_samples=20,
        scheduler=asha_scheduler,
        resources_per_trial={"cpu": 1, "gpu": 0},
        verbose=0,  # 打印详细日志
    )

    print("Tuning a dict-based config finished.")

    # 5. 分析结果
    best_config = analysis.get_best_config(metric="mean_accuracy", mode="max")
    print("\n----------------------------------------------------")
    print("找到的最佳超参数配置:")
    # 打印时，我们只关心被调整的参数
    print({k: v for k, v in best_config.items() if k in search_space})

    best_trial = analysis.get_best_trial(metric="mean_accuracy", mode="max")
    print("\n最佳试验的最终结果:")
    print(f"  - Mean Accuracy: {best_trial.last_result['mean_accuracy']:.4f}")

    ray.shutdown()


if __name__ == "__main__":
    main()
