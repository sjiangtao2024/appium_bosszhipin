from .app_log import BossLog
def jobs_data_output(job_results):
    logger = BossLog(log_name='jobs_data_output')
    total_count = 0
    for key,value in job_results.items():
        if key == '兼职':
            for part_time_key,_ in value.items():
                logger.info(f'{key}{part_time_key}投递数为{len(job_results[key][part_time_key])}')
                total_count += len(job_results[key][part_time_key])
        else:
            logger.info(f'{key}投递数为{len(job_results[key])}')
            total_count += len(job_results[key])
    logger.info(f'总投递数为{total_count}')