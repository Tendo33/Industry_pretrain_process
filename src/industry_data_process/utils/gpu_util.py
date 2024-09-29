import gc
import torch


def release_gpu_memory(llm):
    """
    释放GPU显存，防止内存泄漏
    """
    from vllm.distributed.parallel_state import (
        destroy_model_parallel,
        destroy_distributed_environment,
    )

    destroy_model_parallel()
    destroy_distributed_environment()
    del llm.llm_engine.model_executor.driver_worker
    del llm.llm_engine.model_executor
    del llm
    gc.collect()
    torch.cuda.empty_cache()
    print(f"cuda memory: {torch.cuda.memory_allocated() // 1024 // 1024}MB")
