#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>

struct ThreadData {
    int priority;
    double executionTime;
};

int start = 0;
pthread_mutex_t start_mutex;
pthread_cond_t start_cond;

void* threadFunction(void* arg) {
    struct timeval start_time, end_time;

    pthread_mutex_lock(&start_mutex);
    while (!start) {
        pthread_cond_wait(&start_cond, &start_mutex);
    }
    pthread_mutex_unlock(&start_mutex);

    gettimeofday(&start_time, NULL);

    long long sum = 0;
    for (long long i = 0; i < 10e9; i++) {
        sum += i;
    }

    gettimeofday(&end_time, NULL);
    long seconds = (end_time.tv_sec - start_time.tv_sec);
    long micros = ((seconds * 1000000) + end_time.tv_usec) - (start_time.tv_usec);

    struct ThreadData* data = (struct ThreadData*) arg;
    data->executionTime = micros / 1000.0; 

    return NULL;
}

void executeThreads(int policy, const char* filename) {
    printf("Executing threads with policy %d\n", policy);
    const int numThreads = 8;
    pthread_t threads[numThreads];
    struct ThreadData threadData[numThreads];
    int basePriority = 10;

    pthread_mutex_lock(&start_mutex);
    start = 0;
    pthread_mutex_unlock(&start_mutex);

    for (int i = 0; i < numThreads - 1; i++) { 
        pthread_attr_t attr;
        pthread_attr_init(&attr);
        pthread_attr_setschedpolicy(&attr, policy);

        struct sched_param param;
        pthread_attr_getschedparam(&attr, &param);
        param.sched_priority = basePriority + i * 10;
        pthread_attr_setschedparam(&attr, &param);

        threadData[i].priority = param.sched_priority;

        pthread_create(&threads[i], &attr, threadFunction, &threadData[i]);
        pthread_attr_destroy(&attr);
    }

    threadData[numThreads - 1].priority = -1; 
    pthread_create(&threads[numThreads - 1], NULL, threadFunction, &threadData[numThreads - 1]);

    pthread_mutex_lock(&start_mutex);
    start = 1;
    pthread_cond_broadcast(&start_cond);
    pthread_mutex_unlock(&start_mutex);

    for (int i = numThreads - 1; i >= 0; i--) {
        pthread_join(threads[i], NULL);
    }

    FILE *fp = fopen(filename, "w");
    if (fp == NULL) {
        perror("Error opening file.");
        exit(1);
    }

    for (int i = 0; i < numThreads; i++) {
        if (threadData[i].priority == -1) {
            fprintf(fp, "Default %.2f\n", threadData[i].executionTime);
        } else {
            fprintf(fp, "%d %.2f\n", threadData[i].priority, threadData[i].executionTime);
        }
    }
    fclose(fp);
}

int main() {
    printf("PID = %d\n", getpid());
    pthread_mutex_init(&start_mutex, NULL);
    pthread_cond_init(&start_cond, NULL);

    executeThreads(SCHED_FIFO, "threadDataFIFO.txt");
    executeThreads(SCHED_RR, "threadDataRR.txt");

    pthread_mutex_destroy(&start_mutex);
    pthread_cond_destroy(&start_cond);

    return 0;
}
