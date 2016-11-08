clc;

X = [ 2 , 8 , 32, 128];
Y1_Freepdk =[0.0048413475625; 0.0135007585125;0.051075243575; 0.283865472];
Y2_Freepdk=[0.0048094391125; 0.0135007585125; 0.0435568917; 0.2118510735];
Y3_Freepdk=[0.0047775306625; 0.0129289229375; 0.0419903161125; 0.156997489175];
Y4_Freepdk=[0.0052897701375; 0.0128789376875; 0.0419019176625; 0.1512635205];


Y1_SCN3ME =[0.75276018; 2.08835631; 7.89312366; 40.6931238];
Y2_SCN3ME =[0.74817639; 2.0216187; 6.804401625; 31.6371744];
Y3_SCN3ME =[0.7435926; 2.01449475; 6.62959215; 24.64420014];
Y4_SCN3ME =[0.83660283; 2.0073708; 6.61707036; 23.839544025];

Y1_T_Freepdk =[0.861; 1.32; 1.8; 2.2];
Y2_T_Freepdk =[1.02; 1.33; 1.83; 2.6];
Y3_T_Freepdk =[0.86; 1.5; 1.9; 6.75];
Y4_T_Freepdk =[1.076; 1.34; 2.01; 9.86];

Y1_T_SCN3ME =[9.42; 8.25; 11.69; 12.7];
Y2_T_SCN3ME =[11.82; 16.04; 14.7; 18.21];
Y3_T_SCN3ME =[14.81; 19.24; 23.82; 30.25];
Y4_T_SCN3ME =[22.9; 23.12; 30.75; 44.95];


subplot(4,1,1)
plot (X, Y1_Freepdk, X, Y2_Freepdk, X, Y3_Freepdk, X, Y4_Freepdk,'LineWidth',2);
grid on;
ylabel('Area (mm^2)','FontSize',12, 'Color','k');
xlabel('Total Size (Kbits)','FontSize',12, 'Color','k');
subplot(4,1,2)
plot (X, Y1_SCN3ME, X, Y2_SCN3ME, X, Y3_SCN3ME, X, Y4_SCN3ME,'LineWidth',2);
grid on;
ylabel('Area (mm^2)','FontSize',12, 'Color','k');
xlabel('Total Size (Kbits)','FontSize',12, 'Color','k');
subplot(4,1,3)
plot (X, Y1_T_Freepdk, X, Y2_T_Freepdk, X, Y3_T_Freepdk, X, Y4_T_Freepdk,'LineWidth',2);
grid on;
ylabel('Access time (ns)','FontSize',12, 'Color','k');
xlabel('Total Size (Kbits)','FontSize',12, 'Color','k');
subplot(4,1,4)
plot (X, Y1_T_SCN3ME, X, Y2_T_SCN3ME, X, Y3_T_SCN3ME, X, Y4_T_SCN3ME,'LineWidth',2);
ylabel('Access time (ns)','FontSize',12, 'Color','k');
xlabel('Total Size (Kbits)','FontSize',12, 'Color','k');


grid on;
legend({'16-bit word size', '32-bit word size','64-bit word size',  '128-bit word size'},'Location','northwest','orientation', 'vertical' , 'FontSize',12, 'LineWidth',1.2);



   
   
   
     