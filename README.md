# WeiXinVote
最近看到发的一个微信拉票，闲来无事研究了一下，发现这个活动是可以刷票的，简要的记录一下写刷票脚本的过程。实际上，这种爬虫代码的实现永远都是小问题的，重要的是你要知道别人的页面的逻辑，如何去分析和爬取才是难点

会发现屏幕顶端显示为"本网页由XXX提供"，需要注意的是，这里的"XXX"并不是"mp.weixin.qq.com"，而是S商城的域名。也就是说，这个投票活动的程序是运行在S商城的服务器上面的。这里就涉及到微信公众平台OpenID的概念了。官方对OpenID的解释是：加密后的微信号，每个用户对每个公众号的OpenID是唯一的。

要验证这一点也很容易，只需要通过采用多个微信账号进行投票，并对投票过程进行网络抓包，查看POST中的参数就可以证实。

基于这一点，微信公众平台在转发投票请求时，会在POST参数中包含用户的OpenID；S商城在接收到投票的POST请求后，通过查询当前OpenID是否在4小时已经投过票，就可以阻止单一用户重复投票的行为了。

然而，这里面却存在一个很大的漏洞！

S商城只能判断OpenID是否出现了重复，但是却无法校验OpenID的有效性，因为它是无法调用微信服务器来对这个OpenID进行校验的。

那么我们只需要生成OpenId然后发送post请求就可以了。

但是一次投票也很奇怪，实际上是分两步完成的。第一次是一个get请求

![在这里插入图片描述](https://img-blog.csdnimg.cn/2018120900002716.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3Jhbl9NYXg=,size_16,color_FFFFFF,t_70)

当我看到名字的时候，我以为是这次请求就完成了，但当使用爬虫访问这个页面时，并不能使得票数增加。仔细观察后发现是有另外一个请求。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20181209000041284.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3Jhbl9NYXg=,size_16,color_FFFFFF,t_70)

这个请求的path很奇怪，是一串乱码，而且每次不一样。只触发了第一个请求之后没有再进行其余的操作，所以第一个请求的页面中一定有地方调用了第二个请求。查看源代码时发现在页面中有一串这样的代码

![在这里插入图片描述](https://img-blog.csdnimg.cn/20181208234816338.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3Jhbl9NYXg=,size_16,color_FFFFFF,t_70)
其中有两个参数是第二个请求的path，而那一串颜文字是对js代码的加密，按分号（；）格式化之后直接在chrome控制台中跑，发现这串颜文字代码的效果就是执行第二个请求。

## 总结
到这里基本上就算做完了，剩下的就是代码实现，总的来说，就是访问第一个请求，在页面中爬取参数，将参数作为第二个请求的path进行对第二个请求的访问。
当然还有ip代理，访问的随机的时间间隔，最好能动态模拟不同的设备，即修改User-Agent这些常见问题就不做说明，如果对这些有什么问题可以发邮件。

总的来说，使用python进行代码实现并没有多大的难度，难度在于一步步的分析，掌握网站的逻辑，并不断的尝试。这点只有多做才有效果
