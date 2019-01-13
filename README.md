# AWS_DNS_Cleanup
Cleaning up AWS DNS which are currently not in use.



### Requirments 

``` 
MAKE SURE YOU HAVE DEFAULT REGION DEFINED IN YOUR AWSCLI CONFIGURATION. IF NOT SURE CHECK BY TYPING AWS CONFIGURE
```

code is tested for ```python 2.7```

```
pip install subprocess
pip install awscli
```

Befor running the code make sure you have configure your aws cli. To configure ```AWScli``` run below command on terminal  :
```

aws configure
```

To run the code run ```python route53.py```

## Result
Once the code is exceuted. DNS name which can be deleted is saved in txt file in same folder where the code is save.

```

cat Dns_Not_in_use.txt
```
