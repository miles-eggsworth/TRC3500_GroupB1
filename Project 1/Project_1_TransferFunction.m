clc; clear all; close all;

%% Load Data
data = readmatrix('C:\Users\LENOVO\Desktop\TRC3500\Project_1.csv');  
water_level = data(:,1);  
adc_readings = data(:,2);  
voltage_readings = data(:,3);  

% Water Level vs ADC
coeffs_adc = polyfit(water_level, adc_readings, 1);
adc_fit = polyval(coeffs_adc, water_level);

% Compute R²
SS_res_adc = sum((adc_readings - adc_fit).^2);
SS_tot_adc = sum((adc_readings - mean(adc_readings)).^2);
R2_adc = 1 - (SS_res_adc / SS_tot_adc);

% Compute sensor inaccuracy (highest deviation)
[~, max_idx_adc] = max(abs(adc_readings - adc_fit));
inaccuracy_adc = max(abs(adc_readings - adc_fit));
fprintf('R² for Water Level to ADC: %.4f\n', R2_adc);
fprintf('Sensor Inaccuracy (ADC): %.4f\n', inaccuracy_adc);

% Compute ±10% offset lines
adc_offset_high = polyval([coeffs_adc(1), coeffs_adc(2) * 1.1], water_level);
adc_offset_low = polyval([coeffs_adc(1), coeffs_adc(2) * 0.9], water_level);

% Plot Water Level vs ADC
figure;
scatter(water_level, adc_readings, 'bo', 'MarkerFaceColor', 'b');
hold on;
plot(water_level, adc_fit, 'r-', 'LineWidth', 2);
plot(water_level, adc_offset_high, 'k--', 'LineWidth', 1);
plot(water_level, adc_offset_low, 'k--', 'LineWidth', 1);
plot(water_level(max_idx_adc), adc_readings(max_idx_adc), 'rx', 'MarkerSize', 10, 'LineWidth', 2);
grid on;
xlabel('Water Level (mL)');
ylabel('ADC Reading');
title(sprintf('Water Level to ADC Transfer Function (R² = %.4f)', R2_adc));
legend('Measured Data', 'Fitted Model', '+10%', '-10%', 'Max Deviation');
hold off;

% Water Level vs Voltage
coeffs_voltage = polyfit(water_level, voltage_readings, 1);
voltage_fit = polyval(coeffs_voltage, water_level);

% Compute R²
SS_res_voltage = sum((voltage_readings - voltage_fit).^2);
SS_tot_voltage = sum((voltage_readings - mean(voltage_readings)).^2);
R2_voltage = 1 - (SS_res_voltage / SS_tot_voltage);

% Compute sensor inaccuracy (highest deviation)
[~, max_idx_voltage] = max(abs(voltage_readings - voltage_fit));
inaccuracy_voltage = max(abs(voltage_readings - voltage_fit));
fprintf('R² for Water Level to Voltage: %.4f\n', R2_voltage);
fprintf('Sensor Inaccuracy (Voltage): %.4f V\n', inaccuracy_voltage);

% Compute ±10% offset lines
voltage_offset_high = polyval([coeffs_voltage(1), coeffs_voltage(2) * 1.1], water_level);
voltage_offset_low = polyval([coeffs_voltage(1), coeffs_voltage(2) * 0.9], water_level);

% Plot Water Level vs Voltage
figure;
scatter(water_level, voltage_readings, 'go', 'MarkerFaceColor', 'g'); 
hold on;
plot(water_level, voltage_fit, 'm-', 'LineWidth', 2);
plot(water_level, voltage_offset_high, 'k--', 'LineWidth', 1);
plot(water_level, voltage_offset_low, 'k--', 'LineWidth', 1);
plot(water_level(max_idx_voltage), voltage_readings(max_idx_voltage), 'rx', 'MarkerSize', 10, 'LineWidth', 2);
grid on;
xlabel('Water Level (mL)');
ylabel('Voltage (V)');
title(sprintf('Water Level to Voltage Transfer Function (R² = %.4f)', R2_voltage));
legend('Measured Data', 'Fitted Model', '+10%', '-10%', 'Max Deviation');
hold off;

% ADC vs Voltage
coeffs_adc_voltage = polyfit(adc_readings, voltage_readings, 1);
voltage_fit_adc = polyval(coeffs_adc_voltage, adc_readings);

% Compute R²
SS_res_adc_voltage = sum((voltage_readings - voltage_fit_adc).^2);
SS_tot_adc_voltage = sum((voltage_readings - mean(voltage_readings)).^2);
R2_adc_voltage = 1 - (SS_res_adc_voltage / SS_tot_adc_voltage);

% Compute sensor inaccuracy (highest deviation)
[~, max_idx_adc_voltage] = max(abs(voltage_readings - voltage_fit_adc));
inaccuracy_adc_voltage = max(abs(voltage_readings - voltage_fit_adc));
fprintf('R² for ADC to Voltage: %.4f\n', R2_adc_voltage);
fprintf('Sensor Inaccuracy (ADC to Voltage): %.4f V\n', inaccuracy_adc_voltage);

% Compute ±10% offset lines
voltage_offset_adc_high = polyval([coeffs_adc_voltage(1), coeffs_adc_voltage(2) * 1.1], adc_readings);
voltage_offset_adc_low = polyval([coeffs_adc_voltage(1), coeffs_adc_voltage(2) * 0.9], adc_readings);

% Plot ADC vs Voltage
figure;
scatter(adc_readings, voltage_readings, 'mo', 'MarkerFaceColor', 'm'); 
hold on;
plot(adc_readings, voltage_fit_adc, 'b-', 'LineWidth', 2);
plot(adc_readings, voltage_offset_adc_high, 'k--', 'LineWidth', 1);
plot(adc_readings, voltage_offset_adc_low, 'k--', 'LineWidth', 1);
plot(adc_readings(max_idx_adc_voltage), voltage_readings(max_idx_adc_voltage), 'rx', 'MarkerSize', 10, 'LineWidth', 2);
grid on;
xlabel('ADC Reading');
ylabel('Voltage (V)');
title(sprintf('ADC to Voltage Transfer Function (R² = %.4f)', R2_adc_voltage));
legend('Measured Data', 'Fitted Model', '+10%', '-10%', 'Max Deviation');
hold off;