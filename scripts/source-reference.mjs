/** Shared, fail-closed syntax and checkout-boundary checks for source references.
 * A valid reference is not proof that its content is genuine or still accessible.
 */
import { realpathSync, statSync } from 'node:fs';
import { isAbsolute, relative, resolve, sep } from 'node:path';

export function validHttpsSource(ref) {
  if (typeof ref !== 'string' || ref.includes('\\') || /\s/.test(ref)) return false;
  // URL() silently normalizes some malformed triple-slash URLs.
  if (!/^https:\/\/[^/?#@\s]+/.test(ref)) return false;
  try {
    const url = new URL(ref);
    return url.protocol === 'https:' && !!url.hostname && !url.username && !url.password;
  } catch { return false; }
}

export function validLocalEvidenceFile(ref, repoRoot) {
  if (typeof ref !== 'string' || !ref.trim() || isAbsolute(ref) || ref.includes('\\') || ref.includes('#') || ref.includes('?') || /^[A-Za-z][A-Za-z\d+.-]*:/.test(ref)) return false;
  const full = resolve(repoRoot, ref);
  const rel = relative(repoRoot, full);
  if (rel === '' || rel === '..' || rel.startsWith(`..${sep}`)) return false;
  try {
    // A directory is not evidence; a symlink may point outside the checkout.
    const realRoot = realpathSync(repoRoot);
    const realFile = realpathSync(full);
    const realRel = relative(realRoot, realFile);
    return realRel !== '' && realRel !== '..' && !realRel.startsWith(`..${sep}`) && statSync(realFile).isFile();
  } catch { return false; }
}

export function evidenceReference(ref, repoRoot) {
  return typeof ref === 'string' && ref.startsWith('https://')
    ? validHttpsSource(ref)
    : validLocalEvidenceFile(ref, repoRoot);
}
