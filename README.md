# SpriteSheetMaker
A simple python Sprite sheet maker. It takes separate images and plans them on a new image. Can also export json and yaml files.

Made this for my need in one day.

Maybe will update it in the future

![image](https://user-images.githubusercontent.com/59426055/125518065-cddf3792-cf36-4d44-a761-4b3b562d3830.png)

### Hotkeys: 
F1 = lets you choose a single image and add it into the row (add one row)
F2 = lets you choose a multiple images and add them into the rows (add rows)
F5 = updates 'x' and 'y' cells

## USEGE:

Edit the **row**, **col** and **separate frames (frames)**.
'row' is the row of with the image will be placed on the image, 'col' is for the corresponding column.
Separate frames (frames) is for the nested dict/json/yaml.

The other fields are auto generated.

The x entry is width position and width position plus with of image. It is created by taking the row entry.
The y is corresponding for height.


|  _ |   _                            |        _        |   _  |        _                  | _
--- | ---                           | ---            |---  | ---                      | ---
| x |  \<number in row\> * img.width  | x + img.width  |   y | \<number in col\> * height | y + img.height |

### EXAMPLE:

##### The image below will produce this yaml file:


![image](https://user-images.githubusercontent.com/59426055/125518713-f3f960ae-23ca-468c-bcfc-29dbfe647089.png)

```yaml
Bandit_Idle_1_n0:
  Bandit_Idle_1.png0:
    x: ['32', '64']
    y: ['0', '32']
Bandit_Idle_2_n0:
  Bandit_Idle_2.png1:
    x: ['64', '96']
    y: ['0', '32']
Bandit_Idle_3_n0:
  Bandit_Idle_3.png2:
    x: ['96', '128']
    y: ['0', '32']
Bandit_Idle_4_n0:
  Bandit_Idle_4.png3:
    x: ['128', '160']
    y: ['0', '32']
Bandit_Walk_1_n1:
  Bandit_Walk_1.png4:
    x: ['32', '64']
    y: ['32', '64']
Bandit_Walk_2_n1:
  Bandit_Walk_2.png5:
    x: ['64', '96']
    y: ['32', '64']
Bandit_Walk_3_n1:
  Bandit_Walk_3.png6:
    x: ['96', '128']
    y: ['32', '64']
Bandit_Walk_4_n1:
  Bandit_Walk_4.png7:
    x: ['128', '160']
    y: ['32', '64']
```

##### This will produse:

![image](https://user-images.githubusercontent.com/59426055/125518916-53430e84-a8a9-4d18-bdde-4a693536e5dc.png)


```yaml
frame1:
  Bandit_Idle_1.png0:
    x: ['32', '64']
    y: ['0', '32']
  Bandit_Idle_2.png1:
    x: ['64', '96']
    y: ['0', '32']
  Bandit_Idle_3.png2:
    x: ['96', '128']
    y: ['0', '32']
  Bandit_Idle_4.png3:
    x: ['128', '160']
    y: ['0', '32']
  Bandit_Walk_1.png4:
    x: ['32', '64']
    y: ['32', '64']
  Bandit_Walk_2.png5:
    x: ['64', '96']
    y: ['32', '64']
  Bandit_Walk_3.png6:
    x: ['96', '128']
    y: ['32', '64']
  Bandit_Walk_4.png7:
    x: ['128', '160']
    y: ['32', '64']
```
