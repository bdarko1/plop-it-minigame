#!/usr/bin/env python3
"""Add a 'Watch Ad for Bonus' rewarded video button to the results screen."""
import os, sys

path = os.path.expanduser('~/plop-it-minigame/index.html')
src = open(path).read()

if 'watchAdBtn' in src:
    sys.exit('Ad button already added — nothing to do.')

AD_PLACEMENT_ID = 'ad7660425595729545237'

# ── 1. Add the button to the HTML, right after Play Again ──
html_old = '''        <button class="btn" id="retryBtn">Play Again</button>
        <button class="btn-ghost" id="followBtn">
          Get the full game · @plopit6
        </button>'''

html_new = '''        <button class="btn" id="retryBtn">Play Again</button>
        <button class="btn-ghost" id="watchAdBtn">
          🎬 Watch ad for +50 bonus
        </button>
        <button class="btn-ghost" id="followBtn">
          Get the full game · @plopit6
        </button>'''

assert src.count(html_old) == 1, f"html anchor count={src.count(html_old)}"
src = src.replace(html_old, html_new)

# ── 2. Add the JS handler, right after the existing followBtn listener ──
js_old = '''        followBtn.addEventListener("click", function () {
          console.log("Follow @plopit6 tapped");
        });'''

js_new = '''        followBtn.addEventListener("click", function () {
          console.log("Follow @plopit6 tapped");
        });
        /* ============ Rewarded video ad (TikTok Mini Games monetization) ============ */
        const watchAdBtn = document.getElementById("watchAdBtn");
        let adInProgress = false;
        watchAdBtn.addEventListener("click", function () {
          if (adInProgress) return;
          if (!(window.TTMinis && TTMinis.game && TTMinis.game.createRewardedVideoAd)) {
            console.log("Rewarded ad API unavailable (not running inside TikTok)");
            return;
          }
          adInProgress = true;
          watchAdBtn.disabled = true;
          const originalLabel = watchAdBtn.textContent;
          watchAdBtn.textContent = "Loading ad...";
          try {
            const rewardedAd = TTMinis.game.createRewardedVideoAd({
              adUnitId: "''' + AD_PLACEMENT_ID + '''",
            });
            rewardedAd.onError(function () {
              console.log("Rewarded ad error");
              adInProgress = false;
              watchAdBtn.disabled = false;
              watchAdBtn.textContent = originalLabel;
            });
            rewardedAd.onClose(function (res) {
              adInProgress = false;
              watchAdBtn.disabled = false;
              watchAdBtn.textContent = originalLabel;
              // res.isEnded is true if the user watched the full ad (per TikTok SDK convention)
              if (!res || res.isEnded !== false) {
                score += 50;
                document.getElementById("finalScore").textContent = score;
                watchAdBtn.style.display = "none"; // one bonus per round
              }
            });
            rewardedAd.show().catch(function () {
              console.log("Rewarded ad failed to display");
              adInProgress = false;
              watchAdBtn.disabled = false;
              watchAdBtn.textContent = originalLabel;
            });
          } catch (e) {
            console.log("Rewarded ad exception", e);
            adInProgress = false;
            watchAdBtn.disabled = false;
            watchAdBtn.textContent = originalLabel;
          }
        });'''

assert src.count(js_old) == 1, f"js anchor count={src.count(js_old)}"
src = src.replace(js_old, js_new)

open(path, 'w').write(src)
print("Ad button + handler added successfully")
