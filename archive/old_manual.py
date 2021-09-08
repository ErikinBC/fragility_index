


###############################################################################
# ----------- (2) SPOT CHECK AND FIX INSIG RESULTS WHERE RELEVANT ----------- #

for i in range(1):
    # ---- Type: bbd, ID: 40 ----
    print(stats.fisher_exact([[19,23-19],[12,23-12]])) # 6-month
    print(stats.fisher_exact([[4,23-4],[13,23-13]])) # 6-month (abstract typo)
    print(stats.fisher_exact([[13,23-13],[6,23-6]])) # 12-month
    # ---- Type: bbd, ID: 674 ----
    print(stats.fisher_exact([[2,5],[6,1]]))
    print(stats.chi2_contingency([[2,5],[6,1]],correction=False))
    # ---- Type: bbd, ID: 6577 ----
    print(stats.fisher_exact([[9,8+2],[68,28+9]])[1]) # full vs partial+no
    print(stats.fisher_exact([[9,8],[68,28]])[1]) # full vs partial
    print(stats.chi2_contingency([[9,8,2],[68,28,9]])[1])
    # ---- Type: bbd, ID: 16898 ----
    print(stats.fisher_exact([[9,50-9],[3,50-3]])) # insig 3-months
    print(stats.chi2_contingency([[9,50-9],[3,50-3]],correction=False)) # insig 3-months
    print(stats.fisher_exact([[9,50-9],[1,50-1]])) # sig 6 months
    # ---- Type: bbd, ID: 21436 ----
    print(stats.fisher_exact([[4,13],[11,7]]))
    # ---- Type: bbd, ID: 26684 ----
    print(stats.fisher_exact([[17,44-17],[9,45-9]]))
    # ---- Type: bbd, ID: 30660 ----
    print(stats.fisher_exact([[16,26-16],[26,30 - 26]]))
    print(stats.chi2_contingency([[16,26-16],[26,30 - 26]],correction=False))
    # ---- Type: bbd, ID: 31326 ----
    print(stats.fisher_exact([[8,0],[9,15]]))
    print(stats.fisher_exact([[8,0],[0,3]]))
    # ---- Type: bbd, ID: 31327 ----
    print(stats.fisher_exact([[42,74],[58,26]]))
    print(stats.fisher_exact([[42,58],[74,26]]))
    # ---- Type: bbd, ID: 31616 ----
    print(stats.fisher_exact([[1,16-1],[3,18-3]]))
    print(stats.fisher_exact([[5,16-5],[8,18-8]]))
    # ---- Type: bbd, ID: 34111 ----
    print(stats.fisher_exact([[4, 36], [10, 28]]))
    # ---- Type: bbd, ID: 34240 ----
    print(stats.chi2_contingency([[15,143],[25,120]],False)[1])
    # ---- Type: bbd, ID: 34442 ----
    print(stats.chi2_contingency([[125, 292-125], [54, 158-54]], False)[1])
    # ---- Type: bbd, ID: 34688 ----
    print(stats.fisher_exact([[30, 36-30], [(26+21+20), 33*3-(26+21+20)]]))
    print(stats.fisher_exact([[30, 36 - 30], [20, 33 - 20 ]]))
    # ---- Type: bbd, ID: 34807 ----
    print(stats.chi2_contingency([[54, 70-54], [34, 55-34]],False)[1])
    # ---- Type: bbd, ID: 34906 ----
    print(stats.fisher_exact([[45, 54-45], [35, 60-35]]))
    # ---- Type: bbd, ID: 35024 ----
    # ---- Type: bbd, ID: 35747 ----
    print(stats.fisher_exact([[31, 57 - 31], [3, 26 - 3]]))
    # ---- Type: bbd, ID: 35856 ----
    print(stats.chi2_contingency([[5, 15-5], [4, 38-4]],False)[1])

for ii in range(1):
    # ---- Type: phn, ID: 34 ----
    # ---- Type: phn, ID: 268 ----
    # ---- Type: phn, ID: 410 ----
    print(stats.chi2_contingency([[83, 83-0], [83,83-4]], False)[1])
    # ---- Type: phn, ID: 424 - ---
    print(stats.fisher_exact([[20, 20-4], [20,20-1]]))
    # ---- Type: phn, ID: 432 ----
    print(stats.chi2_contingency([[32,131,45,78], [273 - 32, 1260 - 131, 274 - 45, 1377 - 78]])[1])
    print(stats.chi2_contingency([[32, 131], [273 - 32, 1260 - 131]])[1])
    # ---- Type: phn, ID: 456 ----
    print(stats.chi2_contingency([[21,33-21], [30,35-30]],False))
    # ---- Type: phn, ID: 469 ----
    print(stats.chi2_contingency([[12,18-12], [37,49-37]], False))
    # ---- Type: phn, ID: 496 - ---
    print(stats.chi2_contingency([[10, 47-10], [3,46-3]], False))
    # ---- Type: phn, ID: 613 ----
    print(stats.chi2_contingency([[24,6,41], [53-24,20-6,62-41]]))
    print(stats.chi2_contingency([[20, 8, 10], [53 - 20, 20 - 8, 62 - 10]]))
    # ---- Type: phn, ID: 726 - ---
    print(stats.chi2_contingency([[25, 31], [34-25,34-31]], False))
    print(stats.chi2_contingency([[25, 31], [34 - 25, 34 - 31]], True))
    # ---- Type: phn, ID: 776 ----
    print(stats.chi2_contingency([[22, 25], [26-22, 25-25]], False))
    # ---- Type: phn, ID: 904 ----
    print(stats.chi2_contingency([[16, 25], [44 - 16, 42 - 25]], False))
    # ---- Type: phn, ID: 941 ----
    print(stats.chi2_contingency([[109, 17], [112-109, 19 - 17]], False))
    # ---- Type: phn, ID: 1037 ----
    print(stats.chi2_contingency([[5, 7], [7 -5, 9 - 7]], False))
    # ---- Type: phn, ID: 1047 ----
    # ---- Type: phn, ID: 1049 - ---
    # ---- Type: phn, ID: 1133 ----
    print(stats.chi2_contingency([[3, 6], [45-3, 45-6]], False))
    # ---- Type: phn, ID: 1201 ----
    print(stats.fisher_exact([[17, 35], [43-17, 56-35]]))
    print(stats.fisher_exact([[17, 33], [43 - 17, 56 - 33]]))
    # ---- Type: phn, ID: 1273 ----
    print(stats.chi2_contingency([[21, 21], [30 - 21, 23 - 21]],False))
    # ---- Type: phn, ID: 1286 ----
    print(stats.fisher_exact([[9, 29], [88 - 9, 117 - 29]]))
    # ---- Type: phn, ID: 1473 - ---
    print(stats.chi2_contingency([[20, 12], [28 - 20, 28 - 12]],False))
    # ---- Type: phn, ID: 1572 - ---
    print(stats.chi2_contingency([[12, 1], [18 - 12, 5 - 1]], False))
    # ---- Type: phn, ID: 1702 ----
    print(stats.chi2_contingency([[17, 3], [56-17, 29-3]], False))
    # ---- Type: phn, ID: 1950 ----
    print(stats.chi2_contingency([[12, 8], [25 - 12, 38 - 8]], True))
    # ---- Type: phn, ID: 1973 ----
    print(stats.chi2_contingency([[3, 10], [26 - 3, 26 - 10]], False))
    # ---- Type: phn, ID: 2293 ----
    print(stats.fisher_exact([[15, 22], [8, 1]]))
    # ---- Type: phn, ID: 2405 ----
    # ---- Type: phn, ID: 2437 ----
    # ---- Type: phn, ID: 2745 - ---
    print(stats.chi2_contingency([[45, 40], [5, 1]], False))
