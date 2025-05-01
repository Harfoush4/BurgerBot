# 🍔 BurgerBot

BurgerBot is a robotics project that implements both PID and Fuzzy Logic control algorithms to navigate a two-motor robot using data from a LIDAR sensor. The robot is designed for tasks like right-edge following and general navigation, combining the strengths of both control strategies for reliable autonomous movement.

---

## 🧠 Project Overview

- **Control Algorithms**: PID and Fuzzy Logic
- **Hardware**: Two-motor robot equipped with a LIDAR sensor
- **Primary Goal**: Smooth navigation and edge following, especially using Fuzzy Logic for right-edge following

---

## 📂 Repository Structure

- `PID.py`: PID control algorithm implementation.
- `Fuzzy_right.py`: Fuzzy Logic controller focused on **right-edge following**.
- `Fuzzy_Subsubt.py`: Additional Fuzzy Logic control components for fine-tuning behavior.
- `Context_binding.py`: Manages context-aware decisions.
- `Obs_proj_final.py`: Main control script integrating different modules.
- `Safe_mix.py`: Hybrid control module combining PID and Fuzzy logic.
- `Robot.pptx`: Presentation explaining system architecture, logic, and behavior.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Harfoush4/BurgerBot.git
cd BurgerBot
```

### 2. Install Dependencies
Make sure Python 3 is installed. Then install required packages:
```bash
pip install numpy
```

### 3. Run the Main Script
To launch the robot's control system:
```bash
python Obs_proj_final.py
```

---

## 🎯 Features

- **PID Control**: Precise continuous error-based adjustment.
- **Fuzzy Logic**: Adaptive rule-based control for tasks like edge following.
- **Hybrid System**: Combines the stability of PID with the flexibility of fuzzy logic.
- **LIDAR-based Navigation**: Uses sensor data for reactive, real-time control.

---

## 📊 Performance Highlights

- **Right-Edge Following**: Accurate and smooth tracking of wall edges.
- **Responsiveness**: Fast reactions to dynamic conditions.
- **Noise Resilience**: Robust handling of sensor variation and environmental disturbances.

---

## 📑 Documentation

For detailed logic flow, tuning strategies, and control explanations, refer to the PowerPoint presentation `Robot.pptx` included in this repo.

---

## 👥 Contributing

Contributions are welcome! Please fork the repo and submit a pull request with clear comments and testing if you wish to propose changes.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more info.

---

For more details, visit the [BurgerBot GitHub Repository](https://github.com/Harfoush4/BurgerBot).

