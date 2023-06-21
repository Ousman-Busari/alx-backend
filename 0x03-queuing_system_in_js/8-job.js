function createPushNotificationsJobs(jobs, queue) {
  if (!(jobs instanceof Array)) throw new Error('Jobs is not an array');

  jobs.forEach((jobData) => {
    const job = queue.create('push_notification_code_3', jobData);
    job.save((err) => {
      if (!err) console.log(`Notification job created: ${job.id}`);
    });
    job
      .on('complete', () => {
        console.log(`Notification job ${job.id} completed`);
      })
      .on('failed', (errorMessage) => {
        console.log(`Notification job ${job.id} failed: ${errorMessage}`);
      })
      .on('progress', (progress) => {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      });
  });
}

export default createPushNotificationsJobs;
