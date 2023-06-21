import redis, { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

function setNewSchool(schoolname, value) {
  client.set(schoolname, value, (err, reply) => {
    redis.print(`Reply: ${reply}`);
  });
}

async function displaySchoolValue(schoolname) {
  const getAsync = promisify(client.get).bind(client);
  const reply = await getAsync(schoolname);
  console.log(reply);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
