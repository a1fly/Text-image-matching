// vue.config.js
module.exports = {
  devServer: {
    port: 8081,          // 设置端口
    host: '0.0.0.0',     // 允许外部访问，默认是 'localhost'
    https: false,        // 是否启用 https
    proxy: {             // 配置代理，解决跨域问题
      '/api': {
        target: 'http://localhost:5000',  // 后端 API 地址
        changeOrigin: true,               // 是否改变请求源
        pathRewrite: { '^/api': '' }      // 重写路径
      }
    }
  }
}
