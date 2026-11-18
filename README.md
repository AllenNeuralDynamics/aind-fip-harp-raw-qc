# aind-fip-harp-qc-raw

QC capsule for fiber photometry currently in development. The capsule creates metrics and writes a `quality_control.json`, that can be visualized for manual inspection. More information can be found here: https://github.com/AllenNeuralDynamics/aind-qc-portal.

### Input
The input is a fiber photometry asset acquired following a standard defined here: [Fiber Photometry acquisition standard](https://github.com/AllenNeuralDynamics/aind-file-standards/blob/main/docs/modalities/fip.md).

### Output
The output is a `quality_control.json` that contains several metrics and evaluations for QCing fiber photometry data. In addition, the following list of images are generated in a `qc-raw` folder:

```plaintext
📦 qc-raw
┣ 📜 FipChannelSignalTestSuite_test_sensor_floor_9b8dfc92a....png
┣ 📜 FipChannelSignalTestSuite_test_sensor_floor_9e8ef0e75ce....png
┣ 📜 FipChannelSignalTestSuite_test_sensor_floor_45421a8f7701....png
┣ 📜 FipRawImageTestSuite_test_roi_selection_949f18dc8e364c....png
┣ 📜 FipRawImageTestSuite_test_roi_selection_13331ab500de424....png
┗ 📜 FipRawImageTestSuite_test_roi_selection_ec14e555b6884....png
```
