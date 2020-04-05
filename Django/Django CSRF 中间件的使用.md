### Django CSRF 中间件的使用

<br/>

#### CSRF中间件介绍
* CSRF（Cross Site Request Forgery），中文是跨站点请求伪造，CSRF攻击者在用户已经登录了目标站点后，诱使用户访问一个攻击页面，利用目标网站对于用户的信任，以用户身份在攻击页面对目标网站发起伪造用户操作的请求，达到攻击的目的
* 假设客户登录了某个网站，我写个html诱导客户点击，其实这里是我构造了关注我的接口，如果没有防御措施，就很轻松的完成操作，但是如果我在每次请求时，都需要验证一个随机码，这样便可以避免


<br/>

#### Django CSRF中间件源码阅读
* 本质上Django CSRF是Django的一个中间件，是中间件就需要遵循中间件的规则，有process_view，process_response方法，这个地方有点好奇居然中间件验证不是在process_request中执行，对于不符合要求得直接干掉，而是在这里直接通过，网络上说法不一，唯一稍微认可点的说法是并不是每一个url都需要这个验证，比如说静态图片等
<br/>

* 接着就是process_view函数，其中核心生成token值得代码如下, 结合了随机字符串，安全秘钥，时间等参数进行计算最后得出一个字符串，即为csrf生成的随机值
    ```
    def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    if not using_sysrandom:
        random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    settings.SECRET_KEY)).encode('utf-8')
            ).digest())
    return ''.join(random.choice(allowed_chars) for i in range(length))
    ```

<br/>

* 接下来就是对着csrf值一顿检查，如果不合法，便调用其中的self._reject,如果合法，便调用其中的self._accept，其中如果方法不在这个列表中，便才会检测crsf值，其余方法便是直接调用self._accept
    * 为什么GET方法可以直接通过呢？因为GET方法你要先生成一个crsf随机值给到前端，并且设置cookies，每刷新一次前段的csrf值都会变一次，但是cookies不变，然后你再使用POST等方法提交的时候才能进行检验
    * 提交后只需要把两个值拿过来解密，能解出一样的值就可以了
    * 
    ```
            if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
                if getattr(request, '_dont_enforce_csrf_checks', False):
                    return self._accept(request)

                if request.is_secure():
                    referer = force_text(
                        request.META.get('HTTP_REFERER'),
                        strings_only=True,
                        errors='replace'
                    )
                    if referer is None:
                        return self._reject(request, REASON_NO_REFERER)

                    good_referer = 'https://%s/' % request.get_host()
                    if not same_origin(referer, good_referer):
                        reason = REASON_BAD_REFERER % (referer, good_referer)
                        return self._reject(request, reason)

                if csrf_token is None:
                    return self._reject(request, REASON_NO_CSRF_COOKIE)

                request_csrf_token = ""
                if request.method == "POST":
                    try:
                        request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
                    except IOError:
                        pass

                if request_csrf_token == "":
                    request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')

                if not constant_time_compare(request_csrf_token, csrf_token):
                    return self._reject(request, REASON_BAD_TOKEN)
    ```


<br/>

* 针对以上读完代码感受，自己设计出一套防御系统，需要考虑以下四个方面(仅仅对crsf进行验证，如果本身有xss这样的漏洞存在是不行的)
    * 如何生成token：一定要带入随机值，有不确定性，不然能猜得到的有很大可能被黑客知道规律轻易攻破
    * 如何存储token：可以会话中放一份，cookies中放一份
    * 如何验证token：token都由服务端统一给出去，然后再交互的时候拿回来验证，如果不对，403伺候
    * 如何刷新token：最好是针对每一次特定需要保护的提交刷新一次
    
