import express from 'express';
import bootstrap from './main.server';

// TODO: wire CommonEngine SSR rendering once the app has real routes/content.
const app = express();

app.listen(process.env['PORT'] ?? 4000, () => {
  console.log('marketing-site SSR server placeholder listening');
});

export default bootstrap;
