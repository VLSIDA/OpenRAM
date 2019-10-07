*********************************************
* Transistor Models
* Note: These models are approximate 
*       and should be substituted with actual
*       models from MOSIS or SCN4ME
*       SS model is a copy of nominal with +10% vth0
*********************************************

.MODEL n NMOS (     LEVEL   = 49
+VERSION = 3.1            TNOM    = 27             TOX     = 7.6E-9
+XJ      = 1.5E-7         NCH     = 1.7E17         VTH0    = 0.5108928
+K1      = 0.5307769      K2      = 0.0199705      K3      = 0.2963637
+K3B     = 0.2012165      W0      = 2.836319E-6    NLX     = 2.894802E-7
+DVT0W   = 0              DVT1W   = 5.3E6          DVT2W   = -0.032
+DVT0    = 0.112017       DVT1    = 0.2453972      DVT2    = -0.171915
+U0      = 444.9381976    UA      = 2.921284E-10   UB      = 1.773281E-18
+UC      = 7.067896E-11   VSAT    = 1.130785E5     A0      = 1.1356246
+AGS     = 0.2810374      B0      = 2.844393E-7    B1      = 5E-6
+KETA    = -7.8181E-3     A1      = 0              A2      = 1
+RDSW    = 925.2701982    PRWG    = -1E-3          PRWB    = -1E-3
+WR      = 1              WINT    = 7.186965E-8    LINT    = 1.735515E-9
+XL      = -2E-8          XW      = 0              DWG     = -1.712973E-8
+DWB     = 5.851691E-9    VOFF    = -0.132935      NFACTOR = 0.5710974
+CIT     = 0              CDSC    = 8.607229E-4    CDSCD   = 0
+CDSCB   = 0              ETA0    = 2.128321E-3    ETAB    = 0
+DSUB    = 0.0257957      PCLM    = 0.6766314      PDIBLC1 = 1
+PDIBLC2 = 1.787424E-3    PDIBLCB = 0              DROUT   = 0.7873539
+PSCBE1  = 6.973485E9     PSCBE2  = 1.46235E-7     PVAG    = 0.05
+DELTA   = 0.01           MOBMOD  = 1              PRT     = 0
+UTE     = -1.5           KT1     = -0.11          KT1L    = 0
+KT2     = 0.022          UA1     = 4.31E-9        UB1     = -7.61E-18
+UC1     = -5.6E-11       AT      = 3.3E4          WL      = 0
+WLN     = 1              WW      = 0              WWN     = 1
+WWL     = 0              LL      = 0              LLN     = 1
+LW      = 0              LWN     = 1              LWL     = 0
+CAPMOD  = 2              CGDO    = 1.96E-10       CGSO    = 1.96E-10
+CGBO    = 0              CJ      = 9.276962E-4    PB      = 0.8157962
+MJ      = 0.3557696      CJSW    = 3.181055E-10   PBSW    = 0.6869149
+MJSW    = 0.1            PVTH0   = -0.0252481     PRDSW   = -96.4502805
+PK2     = -4.805372E-3   WKETA   = -7.643187E-4   LKETA   = -0.0129496      )

