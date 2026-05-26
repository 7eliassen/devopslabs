# 5 Лабораторная работа. Мониторинг

В рамках лабораторной работы будет поднят monitoring стек в kubernetes.

Проверим, что helm установлен:
![alt text](screens/image.png)

Добавим репозиторий Prometheus Stack
![alt text](screens/image-2.png)

Установим kube-prometheus-stack
![alt text](screens/image-1.png)

Проверим, что поды успешно запустились:
![alt text](screens/image-3.png)

Пробросим порты и получим доступ к Grafana
![alt text](screens/image-4.png)

Вход осуществляется по логину admin, а пароль необходимо достать из secret

```
kubectl get secret -n monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d
```

![alt text](screens/image-5.png)

Список Dashboards:
![alt text](screens/image-9.png)

Ниже приведены примеры графиков метрик в grafana

![alt text](screens/image-8.png)

![alt text](screens/image-7.png)