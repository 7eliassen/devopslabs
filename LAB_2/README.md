# 2 Лабораторная работа

## 1 часть. Поднимаем kubernetes кластер

В качестве приложения для развертывания будет использован мой менеджер заметок https://github.com/7eliassen/VaultNote/tree/devops-lab

Приложение является состоит из трех составляющих:
- Api
- Frontend
- База данных

### Поднимаем базу данных

Создадим secret для базы данных:
```
kubectl create secret generic db-secret \
  --from-literal=POSTGRES_USER=*** \
  --from-literal=POSTGRES_PASSWORD=*** \
  --from-literal=POSTGRES_DB=***
```

И проверим что он создался

![alt text](screens/1.png)

## 2 часть. HELM