import express from 'express';
import { createQueue } from 'kue';
import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error}`);
});
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

let reservationEnabled;
function reserveSeat(number) {
  return client.set('available_seats', number);
}
async function getCurrentAvailableSeats() {
  const get = promisify(client.get).bind(client);
  return get('available_seats');
}

const queue = createQueue();
const app = express();
const port = 1245;
app.get('/available_seats', async (req, res) => {
  res.json({ numberOfAvailableSeats: await getCurrentAvailableSeats() });
});

app.get('/reserve_seat', async (req, res) => { // eslint-disable-line
  if (reservationEnabled === 'false') {
    return res.json({ status: 'Reservation are blocked' });
  }
  const job = queue.create('reserve_seat', { data: 'reservation info' }).save();
  job
    .on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', (err) => {
      console.log(`Seat reservation job ${job.id} failed: ${err}`);
    })
    .save((err) => {
      if (!err) return res.json({ status: 'Reservation in process' });
      return res.json({ status: 'Reservation failed' });
    });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      done(Error('Not enough seats available'));
    }
    reserveSeat(availableSeats - 1);
    if (availableSeats - 1 === 0) reservationEnabled = false;
    done();
  });
});

app.listen(port, () => {
  reserveSeat(3);
  reservationEnabled = true;
});
