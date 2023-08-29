import { createQueue } from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

const queue = createQueue();

describe('createPushNotificationsJobs', () => {
  before(() => queue.testMode.enter()); /* eslint-disable-line */
  afterEach(() => queue.testMode.clear()); /* eslint-disable-line */
  after(() => queue.testMode.exit()); /* eslint-disable-line */

  it('display a error message if jobs is not an array', () => { /* eslint-disable-line */
    expect(() => createPushNotificationsJobs('jobs', queue)).to.throw(/* eslint-disable-line */
      'Jobs is not an array',
    );
  });

  it('create two new jobs to the queue', () => { /* eslint-disable-line */
    const list = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account',
      },
    ];
    createPushNotificationsJobs(list, queue);
    expect(queue.testMode.jobs.length).to.equal(2); /* eslint-disable-line */
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3'); /* eslint-disable-line */
    expect(queue.testMode.jobs[0].data).to.eql(list[0]); /* eslint-disable-line */
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3'); /* eslint-disable-line */
    expect(queue.testMode.jobs[1].data).to.eql(list[1]); /* eslint-disable-line */
  });
});
