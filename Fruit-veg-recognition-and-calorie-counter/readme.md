# Demo Video

https://github.com/user-attachments/assets/ed7e7e49-693f-4bc2-822e-feba2ca6e6b1

Based on an open-source food recognition project, extended with new features and UI.
About project:
1.)Created a Fruit and vegetable recognition model using transfer learning and mobilenetv2 model, 
2.)Then wrapped that model into django api for model prediction and interaction with webapp
3.)then used django and calorieninjas api to show the calorie and nutritional content of the predicted food


Project startup:

Run both Django apps from PowerShell:

```powershell
.\run_project.ps1
```

Then open:

```text
http://127.0.0.1:8011/
```

Manual startup:

1. Start the model API on port 8010:
   ```powershell
   cd "model api\Fruit_Veg_recognition"
   python manage.py runserver 127.0.0.1:8010 --noreload
   ```

2. Start the calorie web app on port 8011:
   ```powershell
   cd Food_calorie_counter
   $env:MODEL_API_URL='http://127.0.0.1:8010/predict/'
   python manage.py runserver 127.0.0.1:8011 --noreload
   ```
