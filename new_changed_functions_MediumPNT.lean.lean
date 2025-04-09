-- Function: SmoothedChebyshev
   VerticalIntegral' (SmoothedChebyshevIntegrand ψ ε X) 2
 
========================================
-- Function: integrable_x_mul_Smooth1
+    (suppΨ : support ψ ⊆ Icc (1 / 2) 2) (mass_one : ∫ (x : ℝ) in Ioi 0, ψ x / x = 1)
+    (ε : ℝ) (εpos : 0 < ε) :
+    MeasureTheory.IntegrableOn (fun x ↦ x * Smooth1 ψ ε x) (Ioi 0) := by
+  sorry
+
========================================
-- Function: vertical_integrable_Smooth1
+    (suppΨ : support ψ ⊆ Icc (1 / 2) 2) (mass_one : ∫ (x : ℝ) in Ioi 0, ψ x / x = 1)
+    (ε : ℝ) (εpos : 0 < ε) :
+    MeasureTheory.Integrable
+      (fun (y : ℝ) ↦ ∫ (t : ℝ) in Ioi 0, (t : ℂ) ^ (1 + y * I) * (Smooth1 ψ ε t : ℂ)) := by
+  sorry
+
========================================
-- Function: continuousAt_Smooth1
+    (suppΨ : support ψ ⊆ Icc (1 / 2) 2) (mass_one : ∫ (x : ℝ) in Ioi 0, ψ x / x = 1)
+    (ε : ℝ) (εpos : 0 < ε) (y : ℝ) (ypos : 0 < y) :
+    ContinuousAt (fun x ↦ Smooth1 ψ ε x) y := by
+  apply Continuous.continuousAt
+  unfold Smooth1 DeltaSpike MellinConvolution
+  simp only [one_div, ite_mul, one_mul, zero_mul, RCLike.ofReal_real_eq_id, id_eq]
+  sorry
+
 /-%%
 Inserting the Dirichlet series expansion of the log derivative of zeta, we get the following.
 \begin{theorem}[SmoothedChebyshevDirichlet]\label{SmoothedChebyshevDirichlet}
========================================
