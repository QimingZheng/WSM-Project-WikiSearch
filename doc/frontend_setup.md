## Frontend setup 

### Setup

Make sure you have `nodejs ` installed. For faster connection, we recommend `cnpm`

```bash
apt-get install nodejs
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

Enter the front end project directory, install the dependency

```bash
cd app/frontend/
cnpm install
```

Then you can startup a `vue` development server by:

```
vue-cli-service serve
```

This will run the website on `http://localhost:8080"`

Note that we have set proxy server in development(see `vue.config.js`). To start the backend server, run 

```bash
cd app/
python index.py
```

After the server has loaded all files, all things will be on.
