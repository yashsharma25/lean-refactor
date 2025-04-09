-- Function: SmoothedChebyshev
\begin{definition}[SmoothedChebyshev]\label{SmoothedChebyshev}\lean{SmoothedChebyshev}\leanok
Fix $\epsilon>0$, and a bumpfunction $\psi$ supported in $[1/2,2]$. Then we define the smoothed
Chebyshev function $\psi_{\epsilon}$ from $\mathbb{R}_{>0}$ to $\mathbb{C}$ by
$$\psi_{\epsilon}(X) = \frac{1}{2\pi i}\int_{(2)}\frac{-\zeta'(s)}{\zeta(s)}
\mathcal{M}(\widetilde{1_{\epsilon}})(s)
X^{s}ds.$$
\end{definition}
%%-/
noncomputable abbrev SmoothedChebyshevIntegrand (ψ : ℝ → ℝ) (ε : ℝ) (X : ℝ) : ℂ → ℂ :=
  fun s ↦ (- deriv riemannZeta s) / riemannZeta s *
    𝓜 ((Smooth1 ψ ε) ·) s * (X : ℂ) ^ s

========================================
-- Function: integrable_x_mul_Smooth1
lemma integrable_x_mul_Smooth1 {ψ : ℝ → ℝ} (diffΨ : ContDiff ℝ 1 ψ) (ψpos : ∀ (x : ℝ), 0 ≤ ψ x)
    (suppΨ : support ψ ⊆ Icc (1 / 2) 2) (mass_one : ∫ (x : ℝ) in Ioi 0, ψ x / x = 1)
    (ε : ℝ) (εpos : 0 < ε) :
    MeasureTheory.IntegrableOn (fun x ↦ x * Smooth1 ψ ε x) (Ioi 0) := by
  sorry

========================================
-- Function: vertical_integrable_Smooth1
lemma vertical_integrable_Smooth1 {ψ : ℝ → ℝ} (diffΨ : ContDiff ℝ 1 ψ) (ψpos : ∀ (x : ℝ), 0 ≤ ψ x)
    (suppΨ : support ψ ⊆ Icc (1 / 2) 2) (mass_one : ∫ (x : ℝ) in Ioi 0, ψ x / x = 1)
    (ε : ℝ) (εpos : 0 < ε) :
    MeasureTheory.Integrable
      (fun (y : ℝ) ↦ ∫ (t : ℝ) in Ioi 0, (t : ℂ) ^ (1 + y * I) * (Smooth1 ψ ε t : ℂ)) := by
  sorry

========================================
-- Function: continuousAt_Smooth1
lemma continuousAt_Smooth1 {ψ : ℝ → ℝ} (diffΨ : ContDiff ℝ 1 ψ) (ψpos : ∀ (x : ℝ), 0 ≤ ψ x)
    (suppΨ : support ψ ⊆ Icc (1 / 2) 2) (mass_one : ∫ (x : ℝ) in Ioi 0, ψ x / x = 1)
    (ε : ℝ) (εpos : 0 < ε) (y : ℝ) (ypos : 0 < y) :
    ContinuousAt (fun x ↦ Smooth1 ψ ε x) y := by
  apply Continuous.continuousAt
  unfold Smooth1 DeltaSpike MellinConvolution
  simp only [one_div, ite_mul, one_mul, zero_mul, RCLike.ofReal_real_eq_id, id_eq]
  sorry

========================================
