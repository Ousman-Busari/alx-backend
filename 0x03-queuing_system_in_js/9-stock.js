import express from 'express';
import { promisify } from 'util';
import redis, { createClient } from 'redis';

const client = createClient();
client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error}`);
});
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const listProducts = [
  {
    id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4,
  },
  {
    id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10,
  },
  {
    id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2,
  },
  {
    id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5,
  },
];

function getItemById(id) {
  return listProducts.find((item) => item.id === id);
}

function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock, (err, reply) => {
    redis.print(`Reply: ${reply}`);
  });
}
async function getCurrentReservedStockById(itemId) {
  const get = promisify(client.get).bind(client);
  const stock = await get(`item.${itemId}`);
  return stock;
}
function productStat(item) {
  const { stock } = item;
  delete item.stock; // eslint-disable-line
  item.initialAvailableQuantity = stock; // eslint-disable-line
}
listProducts.forEach(productStat);

const app = express();
const port = 1245;

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const item = getItemById(parseInt(req.params.itemId, 10));
  if (item) {
    const stock = await getCurrentReservedStockById(item.id);
    if (!stock) {
      item.currentQuantity = item.initialAvailableQuantity;
    } else {
      item.currentQuantity = item.initialAvailableQuantity - parseInt(stock, 10);
    }
    res.json(item);
  } else {
    res.status(404).json({ status: 'Product not found' });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const item = getItemById(parseInt(req.params.itemId, 10));
  if (!item) res.status(404).json({ status: 'Product not found' });
  else {
    const stock = await getCurrentReservedStockById(item.id);
    if (stock >= item.initialAvailableQuantity) {
      res
        .status(403)
        .json({ status: 'Not enough stock available', itemId: item.id });
    } else {
      console.log(stock);
      if (!stock) {
        reserveStockById(item.id, 1);
      } else {
        reserveStockById(item.id, parseInt(stock, 10) + 1);
      }
      res.json({ status: 'Reservation confirmed', itemId: item.id });
    }
  }
});

app.listen(port, () => {});
